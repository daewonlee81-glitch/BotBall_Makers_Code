@echo off
chcp 65001 >nul
rem 웜뱃 연결 도우미 실행 (Windows) - 더블클릭하세요
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (py -3 wombat-relay.py %*) else (python wombat-relay.py %*)
pause
