@echo off
chcp 65001 > nul
echo === 어드민 동기화 서버 ===
echo 이 창을 열어 두고 어드민에서 "GitHub에 배포" 버튼을 누르세요.
echo 종료하려면 이 창을 닫거나 Ctrl+C 를 누르세요.
echo.
cd /d C:\Users\user\wrong
python tools/sync_server.py
pause
