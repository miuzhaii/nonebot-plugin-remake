#!/usr/bin/env python3
"""
人生重开模拟器 Web 版启动脚本
"""
import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("人生重开模拟器 Web 版")
    print("=" * 60)
    print("启动中...")
    print("访问地址: http://127.0.0.1:8000")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    uvicorn.run(
        "nonebot_plugin_remake.web:web_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
