@echo off
echo Finding uvicorn process...
set "found=0"
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do (
    set "found=1"
    echo Found process with PID: %%a
    taskkill /F /PID %%a 2>nul
    timeout /t 1 /nobreak >nul
    netstat -ano | find ":8000" | find "LISTENING" >nul
    if errorlevel 1 (
        echo Server stopped successfully!
    ) else (
        echo Failed to kill process. Please try again.
    )
)
if %found%==0 (
    echo No uvicorn process found running on port 8000.
)
pause 