"""
测试 HTTP API 的简单脚本
"""
import requests
import sys
from pathlib import Path

BASE_URL = "http://localhost:8000"


def test_random_life():
    """测试完全随机的人生"""
    print("测试 /random 路由...")
    response = requests.get(f"{BASE_URL}/random")
    if response.status_code == 200:
        output_path = Path("test_random_life.jpg")
        output_path.write_bytes(response.content)
        print(f"✓ 成功生成随机人生图片: {output_path}")
        return True
    else:
        print(f"✗ 失败: {response.status_code} - {response.text}")
        return False


def test_talents_info():
    """测试获取天赋信息"""
    print("\n测试 /talents-info 路由...")
    response = requests.get(f"{BASE_URL}/talents-info")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ 成功获取天赋信息，共 {len(data['talents'])} 个天赋")
        for talent in data["talents"][:3]:
            print(f"  - [{talent['id']}] {talent['name']}: {talent['description']}")
        return data["talents"]
    else:
        print(f"✗ 失败: {response.status_code} - {response.text}")
        return None


def test_custom_life():
    """测试自定义人生"""
    print("\n测试 /custom 路由...")
    data = {
        "talent_ids": [0, 1, 2],
        "chr": 5,
        "int": 5,
        "str": 5,
        "mny": 5,
    }
    response = requests.post(f"{BASE_URL}/custom", json=data)
    if response.status_code == 200:
        output_path = Path("test_custom_life.jpg")
        output_path.write_bytes(response.content)
        print(f"✓ 成功生成自定义人生图片: {output_path}")
        return True
    else:
        print(f"✗ 失败: {response.status_code} - {response.text}")
        return False


def test_random_talents():
    """测试随机天赋固定属性"""
    print("\n测试 /random-talents 路由...")
    params = {"chr": 7, "int_val": 6, "str_val": 4, "mny": 3}
    response = requests.get(f"{BASE_URL}/random-talents", params=params)
    if response.status_code == 200:
        output_path = Path("test_random_talents_life.jpg")
        output_path.write_bytes(response.content)
        print(f"✓ 成功生成随机天赋人生图片: {output_path}")
        return True
    else:
        print(f"✗ 失败: {response.status_code} - {response.text}")
        return False


def test_random_attributes():
    """测试固定天赋随机属性"""
    print("\n测试 /random-attributes 路由...")
    params = {"talent_ids": [0, 1, 2]}
    response = requests.get(f"{BASE_URL}/random-attributes", params=params)
    if response.status_code == 200:
        output_path = Path("test_random_attr_life.jpg")
        output_path.write_bytes(response.content)
        print(f"✓ 成功生成随机属性人生图片: {output_path}")
        return True
    else:
        print(f"✗ 失败: {response.status_code} - {response.text}")
        return False


def main():
    """运行所有测试"""
    print("=" * 60)
    print("人生重开模拟器 API 测试")
    print("=" * 60)
    print(f"API 地址: {BASE_URL}")
    print("=" * 60)

    # 检查服务是否启动
    try:
        response = requests.get(BASE_URL, timeout=2)
        print(f"✓ API 服务正在运行\n")
    except requests.exceptions.RequestException as e:
        print(f"✗ 无法连接到 API 服务: {e}")
        print(f"请先启动服务: python app.py")
        sys.exit(1)

    # 运行测试
    results = []
    results.append(("随机人生", test_random_life()))
    results.append(("天赋信息", test_talents_info() is not None))
    results.append(("自定义人生", test_custom_life()))
    results.append(("随机天赋", test_random_talents()))
    results.append(("随机属性", test_random_attributes()))

    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    for name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{name:12s} {status}")

    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\n总计: {passed}/{total} 测试通过")

    if passed == total:
        print("\n✓ 所有测试通过！")
        sys.exit(0)
    else:
        print(f"\n✗ {total - passed} 个测试失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
