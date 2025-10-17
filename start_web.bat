@echo off
REM 人生重开模拟器 Web版 启动脚本 (Windows)

echo ==================================
echo   人生重开模拟器 Web版
echo ==================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.9+
    pause
    exit /b 1
)

echo 检查依赖...
python -c "import fastapi, uvicorn, PIL" >nul 2>&1
if errorlevel 1 (
    echo 警告: 部分依赖未安装
    echo 正在安装依赖...
    pip install -r requirements-web.txt
    if errorlevel 1 (
        echo 错误: 依赖安装失败
        pause
        exit /b 1
    )
)

echo 依赖检查完成！
echo.
echo 启动Web服务器...
echo 访问地址: http://localhost:8000
echo 按 Ctrl+C 停止服务器
echo.

REM 启动服务器
python run_web.py
pause
