# 人生重开模拟器 HTTP API 版本

这是人生重开模拟器的 HTTP API 版本，通过不同的路由返回不同的人生重开结果 PNG 图片。

## 安装依赖

```bash
pip install -r requirements.txt
# 或使用 poetry
poetry install
```

## 启动服务

```bash
# 直接运行
python app.py

# 或使用 uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

服务启动后，访问 http://localhost:8000 查看 API 信息。

## API 文档

启动服务后，可以访问以下地址查看完整的交互式 API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 路由说明

### 1. 完全随机的人生 - `/random`

**方法**: GET

**描述**: 随机选择天赋和属性，返回人生重开结果图片。

**示例**:
```bash
curl http://localhost:8000/random --output random_life.jpg
```

或在浏览器中直接访问: http://localhost:8000/random

---

### 2. 自定义人生 - `/custom`

**方法**: POST

**描述**: 根据指定的天赋和属性，返回人生重开结果图片。

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

**参数说明**:
- `talent_ids`: 选择的3个天赋ID（0-9），需要先通过 `/talents-info` 获取可用天赋
- `chr`: 颜值（0-10）
- `int`: 智力（0-10）
- `str`: 体质（0-10）
- `mny`: 家境（0-10）

**注意**: 属性总和必须等于天赋提供的总属性点。

**示例**:
```bash
curl -X POST http://localhost:8000/custom \
  -H "Content-Type: application/json" \
  -d '{
    "talent_ids": [0, 1, 2],
    "chr": 5,
    "int": 5,
    "str": 5,
    "mny": 5
  }' \
  --output custom_life.jpg
```

---

### 3. 随机天赋，固定属性 - `/random-talents`

**方法**: GET

**描述**: 随机选择天赋，但使用指定的属性值。

**查询参数**:
- `chr`: 颜值（0-10），默认 5
- `int_val`: 智力（0-10），默认 5
- `str_val`: 体质（0-10），默认 5
- `mny`: 家境（0-10），默认 5

**示例**:
```bash
curl "http://localhost:8000/random-talents?chr=7&int_val=6&str_val=4&mny=3" --output random_talents_life.jpg
```

---

### 4. 固定天赋，随机属性 - `/random-attributes`

**方法**: GET

**描述**: 使用指定的天赋，但随机分配属性。

**查询参数**:
- `talent_ids`: 选择的3个天赋ID（0-9），需要重复传递3次

**示例**:
```bash
curl "http://localhost:8000/random-attributes?talent_ids=0&talent_ids=1&talent_ids=2" --output random_attr_life.jpg
```

---

### 5. 获取天赋信息 - `/talents-info`

**方法**: GET

**描述**: 获取一组随机天赋信息，用于查看可用的天赋选项。

**响应示例**:
```json
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

**示例**:
```bash
curl http://localhost:8000/talents-info
```

---

## 使用示例

### Python 客户端示例

```python
import requests
from io import BytesIO
from PIL import Image

# 1. 完全随机的人生
response = requests.get("http://localhost:8000/random")
img = Image.open(BytesIO(response.content))
img.show()
img.save("random_life.jpg")

# 2. 获取天赋信息
response = requests.get("http://localhost:8000/talents-info")
talents = response.json()
print("可用天赋:", talents)

# 3. 自定义人生
data = {
    "talent_ids": [0, 1, 2],
    "chr": 6,
    "int": 5,
    "str": 4,
    "mny": 5
}
response = requests.post("http://localhost:8000/custom", json=data)
img = Image.open(BytesIO(response.content))
img.save("custom_life.jpg")

# 4. 随机天赋，固定属性
response = requests.get("http://localhost:8000/random-talents", params={
    "chr": 7,
    "int_val": 6,
    "str_val": 5,
    "mny": 2
})
img = Image.open(BytesIO(response.content))
img.save("random_talents_life.jpg")

# 5. 固定天赋，随机属性
response = requests.get("http://localhost:8000/random-attributes", params={
    "talent_ids": [0, 1, 2]
})
img = Image.open(BytesIO(response.content))
img.save("random_attr_life.jpg")
```

### JavaScript 客户端示例

```javascript
// 1. 完全随机的人生
fetch('http://localhost:8000/random')
  .then(response => response.blob())
  .then(blob => {
    const url = URL.createObjectURL(blob);
    const img = document.createElement('img');
    img.src = url;
    document.body.appendChild(img);
  });

// 2. 自定义人生
fetch('http://localhost:8000/custom', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    talent_ids: [0, 1, 2],
    chr: 6,
    int: 5,
    str: 4,
    mny: 5
  })
})
  .then(response => response.blob())
  .then(blob => {
    const url = URL.createObjectURL(blob);
    const img = document.createElement('img');
    img.src = url;
    document.body.appendChild(img);
  });
```

## 注意事项

1. **天赋冲突**: 某些天赋之间存在冲突，不能同时选择。如果选择了冲突的天赋，API 会返回错误信息。

2. **属性总和**: 在自定义人生时，属性总和必须等于天赋提供的总属性点，否则会返回错误。

3. **天赋ID**: 天赋ID是随机生成的，每次调用 `/talents-info` 都会得到不同的天赋列表。如果要使用特定天赋，需要先获取天赋信息。

4. **图片格式**: 所有路由返回的都是 JPEG 格式的图片。

## 部署

### Docker 部署

创建 `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
```

构建并运行:
```bash
docker build -t life-remake-api .
docker run -p 8000:8000 life-remake-api
```

### 生产环境部署

使用 Gunicorn + Uvicorn:
```bash
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## 开发

项目结构保持不变，只是添加了 HTTP API 入口：

- `app.py`: HTTP API 入口文件
- `nonebot_plugin_remake/`: 原有的业务逻辑（未修改）
  - `life.py`: 人生模拟核心逻辑
  - `drawer.py`: 图片绘制
  - `talent.py`: 天赋管理
  - `property.py`: 属性管理
  - `event.py`: 事件管理
  - `age.py`: 年龄管理

## 原 NoneBot2 版本

原有的 NoneBot2 插件版本仍然保留在 `nonebot_plugin_remake/__init__.py` 中，可以继续作为 NoneBot2 插件使用。

HTTP API 版本和 NoneBot2 插件版本可以共存，互不影响。
