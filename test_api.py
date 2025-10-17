#!/usr/bin/env python3
"""
测试 Web API 是否正常工作
"""
import time
import requests

BASE_URL = "http://localhost:8000"

def test_api():
    print("=" * 60)
    print("测试人生重开模拟器 Web API")
    print("=" * 60)
    
    try:
        # 1. 开始游戏
        print("\n1. 测试开始游戏...")
        response = requests.get(f"{BASE_URL}/api/start")
        if response.status_code != 200:
            print(f"❌ 失败: {response.status_code}")
            return False
        
        data = response.json()
        session_id = data["session_id"]
        print(f"✓ 成功! Session ID: {session_id}")
        print(f"  获得 {len(data['talents'])} 个天赋")
        print(f"  可用属性点: {data['total_property']}")
        
        # 2. 随机选择天赋
        print("\n2. 测试随机选择天赋...")
        response = requests.post(
            f"{BASE_URL}/api/random-talents",
            json={"session_id": session_id}
        )
        if response.status_code != 200:
            print(f"❌ 失败: {response.status_code}")
            return False
        
        data = response.json()
        print(f"✓ 成功! 选择了天赋: {data['talent_ids']}")
        
        # 3. 随机分配属性
        print("\n3. 测试随机分配属性...")
        response = requests.post(
            f"{BASE_URL}/api/random-property",
            json={"session_id": session_id}
        )
        if response.status_code != 200:
            print(f"❌ 失败: {response.status_code}")
            return False
        
        data = response.json()
        props = data["properties"]
        print(f"✓ 成功! 属性分配: CHR={props['CHR']}, INT={props['INT']}, STR={props['STR']}, MNY={props['MNY']}")
        
        # 4. 运行人生模拟
        print("\n4. 测试运行人生模拟...")
        response = requests.post(
            f"{BASE_URL}/api/run",
            json={"session_id": session_id}
        )
        if response.status_code != 200:
            print(f"❌ 失败: {response.status_code}")
            return False
        
        data = response.json()
        print(f"✓ 成功! 人生共 {len(data['results'])} 年")
        summary = data["summary"]
        print(f"  享年: {summary['AGE']}岁")
        print(f"  总评: {summary['SUM']}")
        
        # 5. 获取图片
        print("\n5. 测试获取图片...")
        response = requests.get(f"{BASE_URL}/api/image/{session_id}")
        if response.status_code != 200:
            print(f"❌ 失败: {response.status_code}")
            return False
        
        data = response.json()
        print(f"✓ 成功! 图片大小: {len(data['image'])} 字符")
        
        print("\n" + "=" * 60)
        print("✓ 所有测试通过!")
        print("=" * 60)
        return True
        
    except requests.exceptions.ConnectionError:
        print("\n❌ 错误: 无法连接到服务器")
        print("   请先运行: python run_web.py")
        return False
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return False

if __name__ == "__main__":
    # 等待一下让服务器启动
    print("等待服务器启动...")
    time.sleep(2)
    
    success = test_api()
    exit(0 if success else 1)
