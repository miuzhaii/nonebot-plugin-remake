# 人生重开模拟器 - Web版本

## 简介

这是人生重开模拟器的Web版本，支持通过浏览器进行游戏，无需聊天机器人环境。

## 功能特性

- ✨ **完整的Web界面**：现代化的响应式UI设计
- 🎮 **开始游戏**：一键开启新的人生模拟
- 🎲 **天赋选择**：从10个随机天赋中选择3个，支持手动选择或随机选择
- 📊 **属性分配**：自由分配颜值、智力、体质、家境属性点
- 🔄 **重启功能**：随时重新开始新的人生
- 📱 **响应式设计**：支持PC和移动端访问
- 🖼️ **结果展示**：生成精美的人生轨迹图片
- 💾 **图片下载**：支持下载生成的人生图片

## 安装依赖

### 使用 Poetry（推荐）

```bash
poetry install
```

### 使用 pip

```bash
pip install fastapi uvicorn[standard] Pillow nonebot2 nonebot-plugin-alconna
```

## 启动Web服务器

### 方法1：使用启动脚本

```bash
python run_web.py
```

### 方法2：使用 uvicorn 命令

```bash
uvicorn nonebot_plugin_remake.web:web_app --host 0.0.0.0 --port 8000 --reload
```

### 方法3：使用 Poetry

```bash
poetry run python run_web.py
```

## 访问游戏

启动服务器后，在浏览器中访问：

```
http://localhost:8000
```

或者从其他设备访问（将 IP 替换为服务器的实际 IP）：

```
http://your-server-ip:8000
```

## 游戏流程

### 1. 开始游戏
点击"开始新游戏"按钮，系统会随机生成10个天赋供你选择。

### 2. 选择天赋
- 从10个随机天赋中选择3个
- 点击天赋卡片进行选择/取消选择
- 可以点击"随机选择"按钮让系统自动选择不冲突的3个天赋
- 某些天赋之间存在冲突，不能同时选择

### 3. 分配属性点
- 拖动滑块分配颜值、智力、体质、家境属性
- 每个属性最高10点，最低0点
- 必须将所有可用属性点分配完毕
- 可以点击"随机分配"按钮让系统自动分配

### 4. 查看结果
- 系统会运行人生模拟，展示你的一生
- 查看每个年龄段发生的事件
- 查看最终的人生总结（享年、各属性评分等）
- 可以下载生成的人生图片作为纪念

### 5. 重新开始
点击"重新开始"按钮，开启新的人生模拟。

## API 接口文档

### 1. 开始游戏
```
GET /api/start
```
返回：session_id、10个随机天赋、可用属性点总数

### 2. 选择天赋
```
POST /api/select-talents
Body: {
    "session_id": "xxx",
    "talent_ids": [0, 1, 2]
}
```

### 3. 随机选择天赋
```
POST /api/random-talents
Body: {
    "session_id": "xxx"
}
```

### 4. 分配属性点
```
POST /api/allocate-property
Body: {
    "session_id": "xxx",
    "properties": {
        "CHR": 5,
        "INT": 5,
        "STR": 5,
        "MNY": 5
    }
}
```

### 5. 随机分配属性
```
POST /api/random-property
Body: {
    "session_id": "xxx"
}
```

### 6. 运行人生模拟
```
POST /api/run
Body: {
    "session_id": "xxx"
}
```

### 7. 获取人生图片
```
GET /api/image/{session_id}
```

### 8. 重启游戏
```
POST /api/restart
Body: {
    "session_id": "xxx"
}
```

## 技术栈

- **后端框架**：FastAPI
- **Web服务器**：Uvicorn
- **图像处理**：Pillow
- **前端**：原生 HTML + CSS + JavaScript
- **设计风格**：现代化渐变UI，响应式布局

## 目录结构

```
nonebot_plugin_remake/
├── web.py              # Web API后端
├── web_static/         # 静态文件目录
│   └── index.html      # 前端页面
├── __init__.py         # NoneBot插件入口
├── life.py            # 人生模拟核心逻辑
├── talent.py          # 天赋管理
├── property.py        # 属性管理
├── event.py           # 事件管理
├── age.py             # 年龄管理
└── drawer.py          # 图片绘制

run_web.py             # Web服务启动脚本
```

## 配置说明

默认配置：
- 端口：8000
- 主机：0.0.0.0（允许外部访问）
- 热重载：开启

如需修改配置，编辑 `run_web.py` 文件中的 `uvicorn.run()` 参数。

## 注意事项

1. **会话管理**：游戏会话存储在内存中，服务器重启后会丢失
2. **并发支持**：支持多用户同时游戏，每个用户有独立的会话
3. **性能考虑**：生成图片需要一定的计算资源，大量并发时可能需要优化
4. **浏览器兼容**：建议使用现代浏览器（Chrome、Firefox、Safari、Edge）

## 开发计划

- [ ] 添加会话持久化（Redis/数据库）
- [ ] 添加用户系统和历史记录
- [ ] 优化图片生成性能
- [ ] 添加更多游戏模式
- [ ] 添加社交分享功能
- [ ] 移动端App版本

## 故障排除

### 问题：启动失败
- 检查端口8000是否被占用
- 确认所有依赖已正确安装
- 查看终端错误信息

### 问题：图片不显示
- 检查资源文件是否完整
- 查看浏览器控制台错误信息
- 确认PIL/Pillow正确安装

### 问题：天赋冲突
- 某些天赋之间天然冲突，这是游戏设计
- 使用"随机选择"功能自动避免冲突

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题，请在 GitHub 仓库提交 Issue。
