@echo off
cd /d "%~dp0"

pyinstaller --noconfirm --clean --onefile --windowed ^
  --name "Disable_HPD_20260309_1" ^
  --icon "Disable_HPD_20260309_1.ico" ^
  --add-data "Disable_HPD_20260309_1.ico;." ^
  "Disable_HPD_20260309_1.py"

pause
