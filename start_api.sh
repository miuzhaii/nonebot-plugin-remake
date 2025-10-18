#!/bin/bash

# 启动人生重开模拟器 HTTP API
echo "🚀 启动人生重开模拟器 HTTP API..."
echo "📡 服务将在 http://0.0.0.0:8000 上运行"
echo "📖 API 文档: http://localhost:8000/docs"
echo ""

# 使用 uvicorn 启动服务
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
