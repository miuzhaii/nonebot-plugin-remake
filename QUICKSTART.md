# 快速开始指南

## Web版本（推荐新手）

### 1. 安装依赖

```bash
pip install -r requirements-web.txt
```

### 2. 启动服务器

#### 方式1：使用启动脚本（最简单）

**Linux/Mac:**
```bash
./start_web.sh
```

**Windows:**
```bash
start_web.bat
```

#### 方式2：直接运行Python脚本
```bash
python run_web.py
```

#### 方式3：使用Poetry（如果你使用Poetry管理依赖）
```bash
poetry install
poetry run python run_web.py
```

### 3. 访问游戏

在浏览器中打开：
```
http://localhost:8000
```

### 4. 开始游戏

1. 点击"开始新游戏"
2. 选择3个天赋（或点击"随机选择"）
3. 分配属性点（或点击"随机分配"）
4. 查看你的人生轨迹
5. 点击"重新开始"再玩一次！

## 功能展示

### 开始界面
- 简洁的欢迎界面
- 一键开始新游戏

### 天赋选择
- 10个随机天赋供选择
- 天赋分为5个等级（普通、优秀、稀有、史诗、传说）
- 支持手动选择或随机选择
- 自动检测天赋冲突

### 属性分配
- 4个属性：颜值、智力、体质、家境
- 直观的滑块控制
- 实时显示剩余点数
- 支持手动分配或随机分配

### 结果展示
- 精美的人生图片
- 详细的年龄事件列表
- 人生总结评分
- 支持下载图片

### 重开功能
- 随时重新开始新的人生
- 保持独立的游戏会话

## 技术特性

- **前后端分离**：后端提供RESTful API，前端使用纯HTML/CSS/JS
- **响应式设计**：支持PC和移动端
- **现代化UI**：渐变色彩，流畅动画
- **多用户支持**：可同时多人游戏，互不干扰
- **会话管理**：每个用户有独立的游戏会话

## API接口

如果你想集成到自己的项目，可以直接调用API：

```javascript
// 开始游戏
GET /api/start

// 选择天赋
POST /api/select-talents
{
    "session_id": "xxx",
    "talent_ids": [0, 1, 2]
}

// 分配属性
POST /api/allocate-property
{
    "session_id": "xxx",
    "properties": {
        "CHR": 5,
        "INT": 5,
        "STR": 5,
        "MNY": 5
    }
}

// 运行模拟
POST /api/run
{
    "session_id": "xxx"
}

// 获取图片
GET /api/image/{session_id}

// 重启游戏
POST /api/restart
{
    "session_id": "xxx"
}
```

## 常见问题

### Q: 端口8000被占用怎么办？
A: 编辑 `run_web.py`，修改 `port=8000` 为其他端口号。

### Q: 如何从其他设备访问？
A: 将 `http://localhost:8000` 中的 `localhost` 替换为服务器的IP地址。

### Q: 图片不显示？
A: 确保 `nonebot_plugin_remake/resources/` 目录下的资源文件完整。

### Q: 如何部署到云服务器？
A: 
1. 上传代码到服务器
2. 安装依赖
3. 运行 `python run_web.py`
4. 配置反向代理（可选，用于HTTPS和域名）

### Q: 支持Docker部署吗？
A: 目前还没有提供Docker镜像，但你可以自己创建Dockerfile：

```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements-web.txt
EXPOSE 8000
CMD ["python", "run_web.py"]
```

## 性能优化建议

1. **生产环境部署**：使用Gunicorn + Uvicorn workers
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker nonebot_plugin_remake.web:web_app
   ```

2. **反向代理**：使用Nginx进行反向代理和负载均衡

3. **会话持久化**：如需支持服务器重启后保持会话，可以集成Redis

4. **图片缓存**：可以将生成的图片缓存到磁盘或CDN

## 下一步

- 查看 [WEB_README.md](WEB_README.md) 了解更多详细信息
- 查看 [README.md](README.md) 了解NoneBot插件版本的使用方法
- 自定义游戏数据：编辑 `nonebot_plugin_remake/resources/data/` 目录下的JSON文件

## 反馈与贡献

遇到问题或有建议？欢迎提交Issue或Pull Request！

祝你玩得开心！🎉
