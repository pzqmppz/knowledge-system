@echo off
REM 口播稿监听脚本启动器 (Windows)

echo ============================================
echo 口播稿自动监听脚本
echo ============================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)

REM 获取脚本所在目录
cd /d "%~dp0"

REM 检查依赖是否安装
python -c "import watchdog" >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖...
    pip install -r watch_voiceover_requirements.txt
    if errorlevel 1 (
        echo 错误: 依赖安装失败
        pause
        exit /b 1
    )
)

REM 运行监听脚本
echo 启动监听脚本...
echo.
python watch_voiceover.py

pause
