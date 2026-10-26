@echo off
rem Opens Claude Code inside the studio with every cache and setting kept in this folder.
where pwsh >nul 2>nul
if %errorlevel%==0 (
  pwsh -NoLogo -NoProfile -File "%~dp0Start-DirectorStudio.ps1"
) else (
  powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0Start-DirectorStudio.ps1"
)
if errorlevel 1 pause
