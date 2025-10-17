#!/usr/bin/env python3
"""
检查系统是否满足运行Web版的要求
"""
import sys
import subprocess

def check_python_version():
    """检查Python版本"""
    print("检查Python版本...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (满足要求: 3.9+)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (需要: 3.9+)")
        return False

def check_module(module_name, package_name=None):
    """检查模块是否安装"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"✓ {package_name} 已安装")
        return True
    except ImportError:
        print(f"✗ {package_name} 未安装")
        return False

def check_all_dependencies():
    """检查所有依赖"""
    print("\n检查依赖包...")
    
    dependencies = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("PIL", "Pillow"),
        ("nonebot", "nonebot2"),
        ("nonebot_plugin_alconna", "nonebot-plugin-alconna"),
    ]
    
    results = []
    for module, package in dependencies:
        results.append(check_module(module, package))
    
    return all(results)

def check_resources():
    """检查资源文件"""
    print("\n检查资源文件...")
    import os
    
    resources_path = os.path.join(
        os.path.dirname(__file__),
        "nonebot_plugin_remake",
        "resources"
    )
    
    if not os.path.exists(resources_path):
        print(f"✗ 资源目录不存在: {resources_path}")
        return False
    
    required_files = [
        "data/age.json",
        "data/events.json",
        "data/talents.json",
    ]
    
    all_exist = True
    for file in required_files:
        file_path = os.path.join(resources_path, file)
        if os.path.exists(file_path):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} 不存在")
            all_exist = False
    
    return all_exist

def main():
    print("=" * 60)
    print("人生重开模拟器 Web版 - 系统需求检查")
    print("=" * 60)
    
    checks = []
    
    # 检查Python版本
    checks.append(check_python_version())
    
    # 检查依赖
    checks.append(check_all_dependencies())
    
    # 检查资源文件
    checks.append(check_resources())
    
    print("\n" + "=" * 60)
    if all(checks):
        print("✓ 所有检查通过！可以运行Web版本。")
        print("\n启动命令:")
        print("  python run_web.py")
        print("  或 ./start_web.sh (Linux/Mac)")
        print("  或 start_web.bat (Windows)")
        print("=" * 60)
        return 0
    else:
        print("✗ 部分检查未通过，请解决以上问题。")
        print("\n安装依赖:")
        print("  pip install -r requirements-web.txt")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
