# Web版安装和故障排除

## 问题说明

Web版本现在使用独立的 `web_app.py` 模块，不依赖NoneBot环境。这样可以避免在运行Web版本时触发NoneBot插件的初始化。

## 快速开始

### 方法1：使用 run_web.py（推荐）

```bash
python run_web.py
```

### 方法2：直接运行 web_app.py

```bash
python web_app.py
```

### 方法3：使用启动脚本

**Linux/Mac:**
```bash
./start_web.sh
```

**Windows:**
```bash
start_web.bat
```

## 文件说明

- `web_app.py` - 独立的Web应用，不依赖NoneBot
- `run_web.py` - Web服务启动脚本（推荐使用）
- `nonebot_plugin_remake/web.py` - 原Web模块（已废弃，使用web_app.py代替）
- `nonebot_plugin_remake/__init__.py` - NoneBot插件入口（仅用于NoneBot环境）

## 常见问题

### Q: 为什么会出现 "NoneBot has not been initialized" 错误？

A: 这是因为导入了 `nonebot_plugin_remake` 包时，`__init__.py` 会被执行，其中包含 NoneBot 相关的初始化代码。Web版本现在使用独立的 `web_app.py`，避免了这个问题。

### Q: 如何同时运行NoneBot插件版和Web版？

A: 可以的！
- NoneBot插件版：在你的NoneBot项目中正常使用
- Web版：使用 `python run_web.py` 或 `python web_app.py` 启动

两者可以同时运行，互不影响。

### Q: Web版需要安装哪些依赖？

A: 
```bash
pip install -r requirements-web.txt
```

或者手动安装：
```bash
pip install fastapi uvicorn[standard] Pillow nonebot2 nonebot-plugin-alconna
```

注意：虽然Web版不需要NoneBot环境运行，但仍然需要安装 `nonebot2` 和 `nonebot-plugin-alconna` 包，因为核心游戏逻辑模块依赖它们的某些工具函数。

### Q: 启动时出现导入错误？

A: 确保你在项目根目录下运行：
```bash
# 正确 ✓
cd /path/to/project
python run_web.py

# 错误 ✗
cd /path/to/project/nonebot_plugin_remake
python ../run_web.py
```

### Q: 如何修改端口？

A: 编辑 `web_app.py` 文件，找到最后的 `uvicorn.run()` 调用：
```python
uvicorn.run(
    web_app,
    host="0.0.0.0",
    port=8000,  # 修改这里
    log_level="info"
)
```

或者编辑 `run_web.py` 文件中的 `port=8000` 参数。

## 架构说明

```
项目结构：

NoneBot插件版:
- nonebot_plugin_remake/__init__.py  (插件入口)
- 需要NoneBot环境

Web独立版:
- web_app.py  (独立应用)
- run_web.py  (启动脚本)
- 不需要NoneBot环境

共享模块:
- nonebot_plugin_remake/life.py      (核心游戏逻辑)
- nonebot_plugin_remake/talent.py    (天赋管理)
- nonebot_plugin_remake/property.py  (属性管理)
- nonebot_plugin_remake/event.py     (事件管理)
- nonebot_plugin_remake/age.py       (年龄管理)
- nonebot_plugin_remake/drawer.py    (图片绘制)
- nonebot_plugin_remake/resources/   (游戏数据)
```

## 开发说明

如果你想修改Web版本：

1. **修改API逻辑**：编辑 `web_app.py`
2. **修改前端界面**：编辑 `nonebot_plugin_remake/web_static/index.html`
3. **修改游戏逻辑**：编辑 `nonebot_plugin_remake/life.py` 等核心模块
4. **测试API**：运行 `python test_api.py`（需要先启动服务器）

## 部署

### Docker部署

```bash
# 使用docker-compose
docker-compose up -d

# 访问
curl http://localhost:8000/api/start
```

### 生产环境部署

使用 Gunicorn + Uvicorn workers：

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker web_app:web_app -b 0.0.0.0:8000
```

### Nginx反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 技术细节

### 为什么需要独立的 web_app.py？

当你导入 `nonebot_plugin_remake.web` 时，Python会执行包的 `__init__.py`，其中包含：

```python
require("nonebot_plugin_alconna")
require("nonebot_plugin_waiter")
```

这些 `require()` 调用需要NoneBot已经初始化（`nonebot.init()`），但在Web模式下我们没有初始化NoneBot，导致错误。

解决方案：创建独立的 `web_app.py`，直接导入需要的核心模块（`life.py`, `drawer.py` 等），跳过包的初始化。

### 核心模块的导入

`web_app.py` 使用以下方式导入：

```python
from nonebot_plugin_remake.drawer import draw_life, save_jpg
from nonebot_plugin_remake.life import Life
from nonebot_plugin_remake.talent import Talent
```

这种方式直接导入模块文件，不会触发 `__init__.py` 的执行。

## 获取帮助

如果遇到问题：

1. 查看 [WEB_README.md](WEB_README.md) - 详细使用文档
2. 查看 [QUICKSTART.md](QUICKSTART.md) - 快速开始指南
3. 运行 `python check_requirements.py` - 检查系统环境
4. 提交 Issue 到 GitHub

## 总结

- ✅ **使用 `python run_web.py` 启动Web版**
- ✅ **Web版和NoneBot插件版可以共存**
- ✅ **独立运行，不需要NoneBot环境初始化**
- ✅ **共享核心游戏逻辑**

祝你玩得开心！🎉
