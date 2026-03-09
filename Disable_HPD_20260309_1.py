# ==============================================================================
#  HPD Presence Sensing Auto-Disable Tool
#  Human Presence Detection 自動關閉工具
# ------------------------------------------------------------------------------
#  Author  : Alex Huang
#  Version : 1.2.0
#  Date    : 2026-03-09
# ------------------------------------------------------------------------------
#  Copyright (c) 2026 Alex Huang. All rights reserved.
# ==============================================================================

import os
import sys
import time
import queue
import locale
import ctypes
import socket
import logging
import threading
import tkinter as tk
from enum import IntEnum
from datetime import datetime
from pathlib import Path

from pywinauto import Desktop, Application
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.uia_element_info import UIAElementInfo


# ------------------------------------------------------------------------------
# App metadata
# ------------------------------------------------------------------------------
APP_NAME = "HPD Presence Sensing Auto-Disable"
APP_NAME_SHORT = "HPD Auto Disable"
APP_VERSION = "1.2.0"
APP_DATE = "2026-03-09"
APP_AUTHOR = "Alex Huang"
APP_COPYRIGHT = "Copyright (c) 2026 Alex Huang. All rights reserved."
APP_ID = "AlexHuang.HPDPresenceSensingAutoDisable"

__author__ = APP_AUTHOR
__version__ = APP_VERSION
__date__ = APP_DATE
__copyright__ = APP_COPYRIGHT


# ------------------------------------------------------------------------------
# Exit codes
# ------------------------------------------------------------------------------
class ExitCode(IntEnum):
    SUCCESS = 0
    SETTINGS_OPEN_FAILED = 10
    TOGGLE_NOT_FOUND = 20
    TOGGLE_SET_FAILED = 30
    UNEXPECTED_ERROR = 99


# ------------------------------------------------------------------------------
# Resource / path helpers
# ------------------------------------------------------------------------------
def get_app_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def get_runtime_base():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return get_app_dir()


def resource_path(*parts):
    return str(get_runtime_base().joinpath(*parts))


APP_DIR = get_app_dir()
RUNTIME_DIR = get_runtime_base()
LOG_DIR = APP_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------------------------
# Windows AppUserModelID for taskbar icon/grouping
# ------------------------------------------------------------------------------
def set_app_user_model_id(app_id=APP_ID):
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        return True
    except Exception:
        return False


# Must be called before creating UI
set_app_user_model_id()


# ------------------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------------------
def build_log_filename():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    host = socket.gethostname()
    pid = os.getpid()
    return LOG_DIR / f"hpd_v{APP_VERSION}_{ts}_{host}_pid{pid}.log"


LOG_FILE = build_log_filename()

logger = logging.getLogger("HPD_Optimization")
logger.setLevel(logging.DEBUG)
logger.handlers.clear()

file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
console_handler = logging.StreamHandler()

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(threadName)s] %(message)s",
    "%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def log(msg, level="INFO"):
    getattr(logger, level.lower(), logger.info)(msg)


def log_section(title):
    log(f"{'=' * 10} {title} {'=' * 10}")


# ------------------------------------------------------------------------------
# UI status window
# ------------------------------------------------------------------------------
_status_thread = None
_status_stop_event = threading.Event()
_status_ready_event = threading.Event()
_status_queue = queue.Queue()


def _load_icon_to_window(root):
    ico = resource_path("app.ico")
    if os.path.exists(ico):
        try:
            root.iconbitmap(ico)
        except Exception as e:
            log(f"設定視窗圖示失敗：{e}", "DEBUG")


def _status_window_worker(message):
    root = None
    try:
        root = tk.Tk()
        root.title(APP_NAME_SHORT)
        root.attributes("-topmost", True)
        root.resizable(False, False)
        root.configure(bg="#F6F8FA")
        root.protocol("WM_DELETE_WINDOW", lambda: None)

        _load_icon_to_window(root)

        win_w = 500
        win_h = 170
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        pos_x = (screen_w - win_w) // 2
        pos_y = (screen_h - win_h) // 2
        root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")

        frame = tk.Frame(root, bg="#F6F8FA", padx=22, pady=18)
        frame.pack(fill="both", expand=True)

        title_lbl = tk.Label(
            frame,
            text="HPD Presence Sensing Auto-Disable",
            font=("Microsoft JhengHei UI", 12, "bold"),
            bg="#F6F8FA",
            fg="#202124"
        )
        title_lbl.pack(pady=(0, 10))

        msg_lbl = tk.Label(
            frame,
            text=message,
            font=("Microsoft JhengHei UI", 11),
            justify="center",
            bg="#F6F8FA",
            fg="#202124"
        )
        msg_lbl.pack()

        hint_lbl = tk.Label(
            frame,
            text="請等待程式完成，自動關閉後再操作電腦。",
            font=("Microsoft JhengHei UI", 9),
            bg="#F6F8FA",
            fg="#5F6368"
        )
        hint_lbl.pack(pady=(12, 0))

        _status_ready_event.set()

        def poll():
            if _status_stop_event.is_set():
                try:
                    root.destroy()
                except Exception:
                    pass
                return

            try:
                new_msg = _status_queue.get_nowait()
                msg_lbl.config(text=new_msg)
            except queue.Empty:
                pass

            root.after(100, poll)

        root.after(100, poll)
        root.mainloop()

    except Exception as e:
        log(f"提示視窗建立失敗：{e}", "WARNING")
        _status_ready_event.set()
    finally:
        if root:
            try:
                root.quit()
            except Exception:
                pass


def show_status_window(message):
    global _status_thread
    _status_stop_event.clear()
    _status_ready_event.clear()

    _status_thread = threading.Thread(
        target=_status_window_worker,
        args=(message,),
        daemon=True,
        name="StatusWindow"
    )
    _status_thread.start()
    _status_ready_event.wait(timeout=2.0)
    time.sleep(0.2)


def update_status_window(message):
    try:
        _status_queue.put_nowait(message)
    except Exception:
        pass


def close_status_window():
    _status_stop_event.set()
    if _status_thread and _status_thread.is_alive():
        _status_thread.join(timeout=2.0)


# ------------------------------------------------------------------------------
# Locale labels
# ------------------------------------------------------------------------------
try:
    raw_locale = locale.getlocale()[0] or "en"
    if "TW" in raw_locale or "Hant" in raw_locale:
        sys_lang = "zh_TW"
    elif "CN" in raw_locale or "Hans" in raw_locale or "SG" in raw_locale:
        sys_lang = "zh_CN"
    else:
        sys_lang = "en"
except Exception as e:
    log(f"語系偵測失敗（{e}），使用預設 en", "WARNING")
    raw_locale = "en"
    sys_lang = "en"

LABELS = {
    "en": [
        "Turn off my screen when I leave",
        "Wake my device when I approach",
        "Dim my screen when I look away",
        "Detect when other people are looking at my screen"
    ],
    "zh_TW": [
        "我離開時關閉螢幕",
        "接近時喚醒此裝置",
        "轉移視線時將螢幕調暗",
        "偵測其他人查看我的螢幕的時間"
    ],
    "zh_CN": [
        "离开时关闭屏幕",
        "接近时唤醒此设备",
        "移开视线时将屏幕调暗",
        "检测其他人查看我的屏幕的时间"
    ]
}

FALLBACK = LABELS.get(sys_lang, LABELS["en"])
log(f"原始 locale：{raw_locale} -> 正規化語系：{sys_lang}")
log(f"使用標籤：{FALLBACK}")


# ------------------------------------------------------------------------------
# UIA helpers
# ------------------------------------------------------------------------------
def get_toggle_state(el):
    try:
        return UIAWrapper(UIAElementInfo(el.element_info.element)).iface_toggle.CurrentToggleState
    except Exception:
        try:
            return el.get_toggle_state()
        except Exception:
            return None


def try_toggle_via_uia(btn):
    try:
        wrapper = UIAWrapper(UIAElementInfo(btn.element_info.element))
        iface = getattr(wrapper, "iface_toggle", None)
        if iface:
            iface.Toggle()
            return True
    except Exception as e:
        log(f"UIA Toggle() 失敗：{e}", "DEBUG")
    return False


def find_toggle_near(text_el):
    log(f"  尋找 '{text_el.window_text()}' 附近的 Toggle...", "DEBUG")
    group = text_el.parent()

    for depth in range(3):
        if not group:
            log(f"  第 {depth} 層父節點為 None，停止搜尋", "DEBUG")
            break

        log(f"  第 {depth} 層父節點：{group.friendly_class_name()} / '{group.window_text()}'", "DEBUG")
        toggles = [
            c for c in group.children()
            if c.friendly_class_name() == "Button" and c.is_visible()
        ]

        log(f"  同層可見 Button 數量：{len(toggles)}", "DEBUG")

        for btn in toggles:
            state = get_toggle_state(btn)
            log(f"    Button '{btn.window_text()}' toggle={state}", "DEBUG")
            if state is not None:
                log(f"  -> 找到 Toggle Button：'{btn.window_text()}' state={state}", "DEBUG")
                return btn

        group = group.parent()

    log("  未找到附近的 Toggle Button", "WARNING")
    return None


# ------------------------------------------------------------------------------
# Main logic
# ------------------------------------------------------------------------------
def ensure_presence_page():
    log_section("確認頁面")
    update_status_window("檢查設定中...\n請勿移動鍵盤或滑鼠")

    log("掃描已開啟的 Settings 視窗...")
    existing = Desktop(backend="uia").windows(class_name="ApplicationFrameWindow")
    log(f"找到 {len(existing)} 個 ApplicationFrameWindow")

    for i, win in enumerate(existing):
        try:
            title = win.window_text()
            log(f"  [{i}] 視窗標題：'{title}'", "DEBUG")
            hdr = win.child_window(title_re=".*Presence.*|.*存在感應.*", control_type="Text")
            if hdr.exists(timeout=0.5):
                log(f"  [{i}] 已在 Presence Sensing 頁，直接使用")
                win.set_focus()
                time.sleep(0.4)
                return win
        except Exception as e:
            log(f"  [{i}] 掃描失敗：{e}", "DEBUG")

    log("未找到已開啟的 Presence 頁，啟動 ms-settings:presence")
    try:
        Application(backend="uia").start("explorer.exe ms-settings:presence")
        log("ms-settings:presence 已送出，等待視窗出現...")

        win = Desktop(backend="uia").window(class_name="ApplicationFrameWindow")
        win.wait("visible ready", timeout=6, retry_interval=0.3)
        win.set_focus()
        time.sleep(1.0)

        log(f"Settings 視窗已就緒，標題：'{win.window_text()}'")
        return win
    except Exception as e:
        log(f"開啟 Settings 失敗：{e}", "ERROR")
        return None


def collect_toggles(win):
    log_section("搜尋 Toggle 按鈕")
    update_status_window("搜尋 Presence Sensing 開關中...\n請勿移動鍵盤或滑鼠")

    found = []

    log("方式①：依語系標籤搜尋")
    for lbl in FALLBACK:
        log(f"  搜尋標籤：'{lbl}'")
        try:
            txt = win.child_window(title=lbl, control_type="Text").wait("exists ready", timeout=0.8)
            log(f"  ✅ 找到文字控制項：'{lbl}'")
            tg = find_toggle_near(txt)

            if tg and tg not in found:
                found.append(tg)
                log(f"  ✅ 新增 Toggle：'{tg.window_text()}' state={get_toggle_state(tg)}")
            elif tg in found:
                log("  ⚠ Toggle 已存在，略過重複", "DEBUG")
        except Exception:
            log(f"  ✗ 找不到標籤 '{lbl}'", "DEBUG")

    log(f"方式① 結果：找到 {len(found)}/4 個")

    if len(found) < 4:
        log("方式②：在 Presence 群組內搜尋")
        try:
            grp = win.child_window(title_re=".*[Pp]resence.*", control_type="Group")
            grp.wait("exists ready", timeout=1.5)
            log(f"  找到群組：'{grp.window_text()}'")

            btns = [
                c for c in grp.descendants(control_type="Button")
                if get_toggle_state(c) is not None
            ]

            log(f"  群組內 Toggle Button 數量：{len(btns)}")
            for b in btns:
                log(f"    Button '{b.window_text()}' state={get_toggle_state(b)} top={b.rectangle().top}", "DEBUG")

            btns.sort(key=lambda x: x.rectangle().top)
            found = btns[:4]
            log(f"方式② 結果：找到 {len(found)} 個")
        except Exception as e:
            log(f"方式② 失敗：{e}", "WARNING")

    if len(found) < 1:
        log("方式③：全頁掃描（排除 top < 100）")
        all_btns = win.descendants(control_type="Button")
        log(f"  全頁 Button 總數：{len(all_btns)}", "DEBUG")

        btns = [
            c for c in all_btns
            if get_toggle_state(c) is not None and c.rectangle().top > 100
        ]

        log(f"  有 TogglePattern 且 top>100 的 Button 數：{len(btns)}")
        for b in btns:
            log(f"    Button '{b.window_text()}' state={get_toggle_state(b)} top={b.rectangle().top}", "DEBUG")

        btns.sort(key=lambda x: x.rectangle().top)
        found = btns[:4]
        log(f"方式③ 結果：找到 {len(found)} 個")

    log(f"最終找到 {len(found)} 個 Toggle 按鈕")
    return found


def process_toggle(btn, idx, total):
    log_section(f"處理 Toggle [{idx + 1}/{total}]")
    update_status_window(
        f"正在關閉 Presence Sensing 開關...\n進度：{idx + 1}/{total}\n請勿移動鍵盤或滑鼠"
    )

    title = btn.window_text()
    rect = btn.rectangle()
    st = get_toggle_state(btn)

    log(f"  title   : '{title}'")
    log(f"  position: top={rect.top} left={rect.left}")
    log(f"  狀態    : {st} ({'ON' if st == 1 else 'OFF' if st == 0 else '未知'})")

    if st == 0:
        log("  -> 已是 OFF，跳過")
        return True

    try:
        btn.set_focus()
    except Exception:
        pass

    if try_toggle_via_uia(btn):
        time.sleep(0.4)
        new_st = get_toggle_state(btn)
        log(f"  UIA 切換後狀態：{new_st}", "DEBUG")
        if new_st == 0:
            log("  ✅ 以 UIA Toggle() 關閉成功")
            return True

    log("  -> 改用 click_input()")
    try:
        btn.click_input()
        time.sleep(0.5)

        new_st = get_toggle_state(btn)
        log(f"  點擊後狀態：{new_st} ({'ON' if new_st == 1 else 'OFF' if new_st == 0 else '未知'})")

        if new_st == 0:
            log("  ✅ 關閉成功")
            return True

        log(f"  ✗ 仍非 OFF（{new_st}）", "WARNING")
        return False
    except Exception as e:
        log(f"  ✗ 點擊失敗：{type(e).__name__}：{e}", "ERROR")
        return False


def run():
    log_section("程式啟動")
    log(f"Tool      : {APP_NAME}")
    log(f"Author    : {APP_AUTHOR}")
    log(f"Version   : {APP_VERSION}")
    log(f"Date      : {APP_DATE}")
    log(f"Python    : {sys.version}")
    log(f"App dir   : {APP_DIR}")
    log(f"Runtime   : {RUNTIME_DIR}")
    log(f"Log file  : {LOG_FILE}")
    log(f"Frozen    : {getattr(sys, 'frozen', False)}")

    win = ensure_presence_page()
    if not win:
        return ExitCode.SETTINGS_OPEN_FAILED

    toggles = collect_toggles(win)
    if not toggles:
        return ExitCode.TOGGLE_NOT_FOUND

    log_section("開始處理")
    success = 0
    total = len(toggles)

    for i, t in enumerate(toggles):
        if process_toggle(t, i, total):
            success += 1

    log_section("執行結果")
    log(f"成功：{success} / 共：{len(toggles)}")

    if success != len(toggles):
        return ExitCode.TOGGLE_SET_FAILED

    return ExitCode.SUCCESS


def show_result_message(exit_code, elapsed):
    if exit_code == ExitCode.SUCCESS:
        title = "執行完畢 ✅"
        text = (
            "所有 Presence Sensing 開關已關閉！\n"
            f"總執行時間：{elapsed:.1f} 秒\n"
            f"Log：{LOG_FILE.name}"
        )
        flags = 0x40 | 0x40000
    else:
        title = "執行失敗 ❌"
        text = (
            "有錯誤發生，請查看 log 檔。\n"
            f"錯誤碼：{int(exit_code)}\n"
            f"總執行時間：{elapsed:.1f} 秒\n"
            f"Log：{LOG_FILE.name}"
        )
        flags = 0x10 | 0x40000

    ctypes.windll.user32.MessageBoxW(0, text, title, flags)


if __name__ == "__main__":
    start_time = time.time()
    exit_code = ExitCode.UNEXPECTED_ERROR

    show_status_window("檢查設定中...\n請勿移動鍵盤或滑鼠")

    try:
        exit_code = run()
    except Exception as e:
        log(f"未預期錯誤：{type(e).__name__}：{e}", "ERROR")
        exit_code = ExitCode.UNEXPECTED_ERROR
    finally:
        close_status_window()

    elapsed = time.time() - start_time

    log_section("程式結束")
    log(f"總執行時間：{elapsed:.1f} 秒")
    log(f"結果碼：{int(exit_code)}")
    log(f"結果：{'成功 ✅' if exit_code == ExitCode.SUCCESS else '失敗 ❌'}")

    show_result_message(exit_code, elapsed)
    sys.exit(int(exit_code))
