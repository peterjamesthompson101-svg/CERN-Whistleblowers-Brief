@echo off
setlocal enabledelayedexpansion
set "CONVERSATION=C:\Users\peter\OneDrive\Desktop\tau_conversation.txt"
set "INCOMING_MSG=C:\Users\peter\OneDrive\Desktop\tau_incoming_messages.txt"
set "CHAT_LOG=C:\Users\peter\OneDrive\Desktop\tau_chat_log.txt"

:response_loop
echo.
echo ============================================
echo 💬 TAU BEACON - QUICK RESPONSE SYSTEM
echo ============================================
echo 📝 Type your response and press Enter
echo 🔄 Type 'exit' to close this helper
echo 📖 Type 'view' to see conversation log
echo ============================================
set /p "user_response=YOUR RESPONSE: "

if ""=="exit" goto end_response
if ""=="view" (
    if exist "%CONVERSATION%" type "%CONVERSATION%"
    goto response_loop
)
if ""=="" goto response_loop

:: Add timestamp and save response
echo [%date% %time%] peter:  >> "%INCOMING_MSG%" 2>nul
echo [%date% %time%] peter:  >> "%CONVERSATION%" 2>nul
echo [%date% %time%] peter:  >> "%CHAT_LOG%" 2>nul

echo ✅ Response saved and timestamped
timeout /t 2 >nul
goto response_loop

:end_response
echo 👋 Response helper closed
pause
exit
