# 人生重开模拟器 - HTTP API 版本

## 🎯 项目说明

本项目已支持 **HTTP API** 模式，保持原有 NoneBot2 插件功能不变的同时，新增了基于 FastAPI 的 HTTP API 接口。通过访问不同的路由，可以获取不同的人生重开结果 PNG 图片。

## ✨ 特性

- ✅ **保留原功能**：NoneBot2 插件功能完全保留，可继续使用
- ✅ **新增 HTTP API**：通过 RESTful API 方式调用人生重开功能
- ✅ **多种模式**：支持完全随机、自定义天赋和属性、半随机等多种模式
- ✅ **返回图片**：所有路由均返回 PNG 格式的人生结果图片
- ✅ **交互式文档**：自动生成 Swagger UI 和 ReDoc 文档

## 🚀 快速开始

### 安装依赖

```bash
# 方式 1: 使用 pip
pip install -r requirements.txt

# 方式 2: 使用 uv (推荐)
uv pip install -r requirements.txt
```

### 启动服务

```bash
# 方式 1: 使用启动脚本
./start_api.sh

# 方式 2: 直接运行
python app.py

# 方式 3: 使用 uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 访问 API

服务启动后，可以通过以下方式访问：

- **API 根路径**: http://localhost:8000/
- **交互式文档 (Swagger UI)**: http://localhost:8000/docs
- **API 文档 (ReDoc)**: http://localhost:8000/redoc

## 📡 API 路由

### 1. GET `/random` - 完全随机的人生

随机选择天赋和属性，返回人生结果图片。

**示例**:
```bash
curl http://localhost:8000/random --output random_life.jpg

# 或直接在浏览器访问
open http://localhost:8000/random
```

### 2. POST `/custom` - 自定义人生

根据指定的天赋和属性，返回人生结果图片。

**请求体**:
```json
{
  "talent_ids": [0, 1, 2],
  "chr": 5,
  "int": 5,
  "str": 5,
  "mny": 5
}
```

**示例**:
```bash
curl -X POST http://localhost:8000/custom \
  -H "Content-Type: application/json" \
  -d '{"talent_ids":[0,1,2],"chr":5,"int":5,"str":5,"mny":5}' \
  --output custom_life.jpg
```

### 3. GET `/random-talents` - 随机天赋，固定属性

随机选择天赋，使用指定的属性值。

**参数**:
- `chr`: 颜值 (0-10)
- `int_val`: 智力 (0-10)
- `str_val`: 体质 (0-10)
- `mny`: 家境 (0-10)

**示例**:
```bash
curl "http://localhost:8000/random-talents?chr=7&int_val=6&str_val=4&mny=3" \
  --output random_talents.jpg
```

### 4. GET `/random-attributes` - 固定天赋，随机属性

使用指定的天赋，随机分配属性。

**参数**:
- `talent_ids`: 天赋ID列表 (需要传递3次)

**示例**:
```bash
curl "http://localhost:8000/random-attributes?talent_ids=0&talent_ids=1&talent_ids=2" \
  --output random_attr.jpg
```

### 5. GET `/talents-info` - 获取天赋信息

获取一组随机天赋信息，用于选择天赋。

**示例**:
```bash
curl http://localhost:8000/talents-info

# 返回 JSON 格式
{
  "talents": [
    {
      "id": 0,
      "name": "天生丽质",
      "description": "你拥有出众的外貌",
      "grade": 2
    },
    ...
  ],
  "note": "每次请求会生成不同的随机天赋列表"
}
```

## 🌐 Web 演示页面

项目包含一个 HTML 演示页面 (`demo.html`)，可以直接在浏览器中测试所有 API 功能。

使用方法：
1. 启动 API 服务
2. 在浏览器中打开 `demo.html` 文件
3. 点击不同按钮测试各种功能

## 🐳 Docker 部署

### 构建镜像

```bash
docker build -t life-remake-api .
```

### 运行容器

```bash
# 方式 1: 直接运行
docker run -p 8000:8000 life-remake-api

# 方式 2: 使用 docker-compose
docker-compose up -d
```

### 停止服务

```bash
docker-compose down
```

## 📁 项目结构

```
.
├── app.py                          # HTTP API 入口文件 (新增)
├── start_api.sh                    # 启动脚本 (新增)
├── requirements.txt                # Python 依赖 (更新)
├── demo.html                       # Web 演示页面 (新增)
├── Dockerfile                      # Docker 配置 (新增)
├── docker-compose.yml              # Docker Compose 配置 (新增)
├── README_API.md                   # API 详细文档 (新增)
├── API_使用说明.md                 # 本文件
├── nonebot_plugin_remake/
│   ├── __init__.py                 # NoneBot 插件入口 (已修改，支持跳过初始化)
│   ├── life.py                     # 人生模拟核心逻辑
│   ├── drawer.py                   # PNG 图片绘制
│   ├── talent.py                   # 天赋管理
│   ├── property.py                 # 属性管理
│   ├── event.py                    # 事件管理
│   ├── age.py                      # 年龄管理
│   ├── utils.py                    # 工具函数 (已修改，支持无 NoneBot)
│   └── resources/                  # 数据资源文件
│       ├── data/                   # JSON 数据
│       ├── fonts/                  # 字体文件
│       └── images/                 # 图片资源
└── test_api.py                     # API 测试脚本 (新增)
```

## 🔧 开发说明

### 原理

项目通过环境变量 `SKIP_NONEBOT_INIT` 控制是否加载 NoneBot 相关代码：

- 当设置 `SKIP_NONEBOT_INIT=1` 时，跳过 NoneBot 初始化，仅加载核心业务逻辑
- 在 `app.py` 中设置了该环境变量，因此可以直接导入和使用业务逻辑模块
- 原有的 NoneBot2 插件功能不受影响，可以继续正常使用

### 核心模块

以下模块是独立的，不依赖 NoneBot：

- `life.py` - 人生模拟引擎
- `drawer.py` - 图片绘制
- `talent.py` - 天赋系统
- `property.py` - 属性系统
- `event.py` - 事件系统
- `age.py` - 年龄系统

### 扩展开发

如需添加新的 API 路由，只需在 `app.py` 中：

1. 定义新的路由函数
2. 调用 `run_life_simulation()` 函数生成人生
3. 返回生成的图片

示例：
```python
@app.get("/my-custom-route")
async def my_custom_life():
    # 自定义参数
    img = run_life_simulation(
        talent_ids=[0, 1, 2],
        chr=8, int_val=8, str_val=4, mny=0
    )
    img.seek(0)
    return StreamingResponse(img, media_type="image/jpeg")
```

## 🧪 测试

运行测试脚本：

```bash
# 确保 API 服务已启动
python test_api.py
```

测试脚本会：
1. 检查 API 服务是否运行
2. 测试所有路由
3. 生成测试图片
4. 输出测试结果

## 🐛 故障排除

### 问题1: 端口被占用

```bash
# 修改 app.py 中的端口
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)  # 改为其他端口
```

### 问题2: 图片生成失败

确保以下文件存在：
- `nonebot_plugin_remake/resources/data/*.json`
- `nonebot_plugin_remake/resources/fonts/方正像素12.ttf`
- `nonebot_plugin_remake/resources/images/*`

### 问题3: 依赖安装失败

```bash
# 使用虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 重新安装依赖
pip install -r requirements.txt
```

## 📝 注意事项

1. **天赋冲突**: 某些天赋之间存在冲突，不能同时选择
2. **属性总和**: 自定义人生时，属性总和必须等于天赋提供的总属性点
3. **天赋ID**: 每次调用 `/talents-info` 都会生成新的随机天赋列表
4. **图片格式**: 所有路由返回的都是 JPEG 格式图片

## 📚 更多文档

- **详细 API 文档**: 查看 `README_API.md`
- **原项目 README**: 查看 `README.md`
- **交互式 API 文档**: 启动服务后访问 http://localhost:8000/docs

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
