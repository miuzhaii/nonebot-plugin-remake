"""
人生重开模拟器 - 独立运行模块
可以作为独立的Web应用运行，无需NoneBot环境
"""
import uvicorn
from .web import web_app

if __name__ == "__main__":
    print("=" * 60)
    print("人生重开模拟器 - Web版")
    print("=" * 60)
    print("启动中...")
    print("访问地址: http://127.0.0.1:8000")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    uvicorn.run(
        web_app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
