@echo off
REM One-click setup script for Windows

echo 🏈 Fantasy Football Social - Easy Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed!
    echo 📥 Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo ✓ Dependencies installed!
) else (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.

REM Ask if user wants test data
set /p create_test="Would you like to create test data? (y/n): "
if /i "%create_test%"=="y" (
    echo 📊 Creating test data...
    python create_test_data.py
    echo ✓ Test data created!
    echo.
    echo Test usernames: fantasy_guru, the_commish, waiver_wire_king, taco_tuesday, analytics_andy
)

echo.
echo 🚀 Starting the app...
echo 📱 The app will open in your browser automatically
echo 🔗 If not, go to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the app
echo.

REM Run the app
streamlit run app.py

pause
