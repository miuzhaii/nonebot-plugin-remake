"""
人生重开模拟器 - 独立运行模块
可以作为独立的Web应用运行，无需NoneBot环境

注意：请使用 run_web.py 启动Web版本
"""
import sys
from pathlib import Path

if __name__ == "__main__":
    print("=" * 60)
    print("人生重开模拟器 - Web版")
    print("=" * 60)
    print("\n请使用以下命令启动Web版本:")
    print("  python run_web.py")
    print("  或 python web_app.py")
    print("\n直接运行此模块会加载NoneBot依赖，可能导致错误。")
    print("=" * 60)
    
    sys.exit(1)
