# Disable HPD

Disable HPD is a Windows automation tool for turning off **Human Presence Detection (HPD)** / Presence Sensing related settings automatically.

本工具會自動開啟 Windows 設定中的 Presence Sensing 頁面，並嘗試將相關開關關閉，方便快速停用 HPD 功能。

---

## Features

- Auto open `ms-settings:presence`
- Auto detect Presence Sensing related toggles
- Support English / Traditional Chinese / Simplified Chinese UI labels
- Show an on-screen status window during execution
- Generate UTF-8 log files automatically
- Return exit codes for debugging or batch execution
- Support packaging into a standalone EXE

---

## Use Cases

This tool is useful when you want to disable behaviors such as:

- Turn off my screen when I leave
- Wake my device when I approach
- Dim my screen when I look away
- Detect when other people are looking at my screen

---

## Project Files

```text
Disable_HPD_20260309_1.py
Disable_HPD_20260309_1.ico
README.md
logs/
```


---

## Requirements

- Windows 11
- A device / system build that includes Presence Sensing settings
- Python 3.x
- `pywinauto`

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

- Please do not move the mouse while the tool is running.
- Please do not press the keyboard during automation.
- Please do not switch windows during execution.
- If Windows Settings UI changes, the automation may need to be updated.

---

## Logs

Log files are generated automatically in the `logs` folder.

Example filename:

```text
hpd_v1.2.0_YYYYMMDD_HHMMSS_HOSTNAME_pid1234.log
```

Logs include:

- Startup information
- Locale detection result
- Settings window detection
- Toggle search process
- Toggle state changes
- Error details

---

## Exit Codes

| Code | Meaning |
| :-- | :-- |
| 0 | Success |
| 10 | Failed to open Presence settings page |
| 20 | Toggle buttons not found |
| 30 | Failed to turn off one or more toggles |
| 99 | Unexpected error |


---

## Limitations

- This tool depends on the Windows Settings UI structure.
- Different OEM devices may show different Presence Sensing layouts.
- If the device does not support HPD, related settings may not exist.
- Future Windows UI changes may require code updates.

---

## Copyright

Copyright (c) 2026 Alex Huang. All rights reserved.

This software is the personal work of Alex Huang.
Unauthorized copying, modification, distribution, or commercial use is strictly prohibited.

---

## Author

Alex Huang

