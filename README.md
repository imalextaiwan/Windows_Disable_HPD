A Windows automation tool to quickly disable Human Presence Detection (HPD) and Presence Sensing settings.

本工具旨在自動開啟 Windows 的「存在感應 (Presence Sensing)」設定頁面，並自動將相關的偵測開關切換為關閉狀態。

---

## Features

- Auto open `ms-settings:presence`
- Auto detect and turn off Presence Sensing related toggles
- Support English / Traditional Chinese / Simplified Chinese UI labels
- Show an on-screen status window during execution
- Generate UTF-8 log files automatically
- Return exit codes for debugging or batch execution
- Support packaging into a standalone EXE via PyInstaller

---

## Use Cases

This tool disables the following Presence Sensing behaviors:

- Turn off my screen when I leave
- Wake my device when I approach
- Dim my screen when I look away
- Detect when other people are looking at my screen

---

## Project Files

```text
Disable_HPD_20260309_1.py   Python 原始程式
Disable_HPD_20260309_1.ico  程式圖示
readme.txt                  使用說明（給一般使用者）
README.md                   GitHub 專案說明
logs/                       執行記錄資料夾（執行後自動產生）
```

---

## Requirements

- Windows 11
- A device that supports Presence Sensing settings
- Python 3.x
- pywinauto

Install dependency:

```bash
pip install pywinauto
```

---

## Run with Python

```bash
python Disable_HPD_20260309_1.py
```

---

## Build EXE with PyInstaller

```bash
pyinstaller --noconfirm --clean --onefile --windowed ^
  --name "Disable_HPD_20260309_1" ^
  --icon "Disable_HPD_20260309_1.ico" ^
  --add-data "Disable_HPD_20260309_1.ico;." ^
  "Disable_HPD_20260309_1.py"
```

After build, the EXE will be generated in the `dist` folder.

---

## Usage Notes

- Do not move the mouse while the tool is running
- Do not press the keyboard during automation
- Do not switch windows during execution
- If the Windows Settings UI changes, the automation may need to be updated

---

## Logs

Log files are generated automatically in the `logs` folder after each run.

Example filename:

```text
hpd_v1.2.0_YYYYMMDD_HHMMSS_HOSTNAME_pid1234.log
```

Logs include startup info, locale detection, toggle search process, state changes, and error details.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 10 | Failed to open Presence settings page |
| 20 | Toggle buttons not found |
| 30 | Failed to turn off one or more toggles |
| 99 | Unexpected error |

---

## Limitations

- Depends on Windows Settings UI structure
- Different OEM devices may show different Presence Sensing layouts
- If the device does not support HPD, related settings may not exist
- Future Windows UI changes may require code updates

---

## License

MIT License

Copyright (c) 2026 Alex Huang

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Author
Alex Huang — github.com/imalextaiwan
```
