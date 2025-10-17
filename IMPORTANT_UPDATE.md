# ⚠️ 重要更新 - Web版本架构调整

## 更新说明

为了解决 Web 版本与 NoneBot 环境的兼容性问题，我们对架构进行了调整。

### 之前的问题

运行 `python run_web.py` 时可能会遇到以下错误：
```
ValueError: NoneBot has not been initialized.
RuntimeError: Cannot load plugin "nonebot_plugin_waiter"!
```

### 解决方案

创建了独立的 **`web_app.py`** 模块，不依赖 NoneBot 环境初始化。

### 现在如何使用

**没有任何变化！** 使用方式完全相同：

```bash
# 方法1（推荐）
python run_web.py

# 方法2
python web_app.py

# 方法3
./start_web.sh  # Linux/Mac
start_web.bat   # Windows
```

访问 http://localhost:8000 即可！

### 技术细节

- ✅ 新增：`web_app.py` - 独立的 Web 应用入口
- ✅ 更新：`run_web.py` - 现在启动 `web_app.py` 而不是 `nonebot_plugin_remake.web`
- ✅ 保持：所有核心游戏逻辑和前端界面不变
- ✅ 兼容：NoneBot 插件版和 Web 版可以同时使用

### 功能变化

**无任何功能变化！** 

- ✅ 所有API接口保持不变
- ✅ 前端界面保持不变
- ✅ 游戏逻辑保持不变
- ✅ 使用方式保持不变

### 为什么需要这个更新？

当导入 `nonebot_plugin_remake` 包时，会自动加载 NoneBot 插件系统，需要 NoneBot 环境。Web 版本不需要 NoneBot，所以我们创建了独立的入口点。

### 需要重新安装吗？

**不需要！** 如果你已经安装了依赖，直接使用即可。

如果是首次使用，安装依赖：
```bash
pip install -r requirements-web.txt
```

### 遇到问题？

请查看 [WEB_SETUP.md](WEB_SETUP.md) 获取详细的故障排除指南。

---

**更新日期**: 2024
**影响范围**: Web 版本启动方式
**是否需要操作**: 否（自动适配）
