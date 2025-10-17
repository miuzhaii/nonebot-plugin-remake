#!/bin/bash
# 人生重开模拟器 Web版 启动脚本

echo "=================================="
echo "  人生重开模拟器 Web版"
echo "=================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装 Python 3.9+"
    exit 1
fi

# 检查是否安装了依赖
echo "检查依赖..."
python3 -c "import fastapi, uvicorn, PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "警告: 部分依赖未安装"
    echo "正在安装依赖..."
    pip3 install -r requirements-web.txt
    if [ $? -ne 0 ]; then
        echo "错误: 依赖安装失败"
        exit 1
    fi
fi

echo "依赖检查完成！"
echo ""
echo "启动Web服务器..."
echo "访问地址: http://localhost:8000"
echo "按 Ctrl+C 停止服务器"
echo ""

# 启动服务器
python3 run_web.py
