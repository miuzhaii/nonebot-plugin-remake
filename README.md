# nonebot-plugin-remake

适用于 [Nonebot2](https://github.com/nonebot/nonebot2) 的人生重开模拟器

这垃圾人生一秒也不想待了？立即重开！

## 🌟 新增：Web版本

现在支持独立的Web版本！无需NoneBot环境，直接通过浏览器玩游戏！

### 快速开始 Web 版

```bash
# 安装依赖
pip install -r requirements-web.txt

# 启动服务器
python run_web.py

# 或使用启动脚本
./start_web.sh          # Linux/Mac
start_web.bat           # Windows
```

访问 http://localhost:8000 即可开始游戏！

📖 详细的Web版使用说明请查看 [WEB_README.md](WEB_README.md)

---

## NoneBot 插件版本


### 安装

- 使用 nb-cli

```
nb plugin install nonebot_plugin_remake
```

- 使用 pip

```
pip install nonebot_plugin_remake
```


### 使用

#### 触发方式：

**以下命令需要加[命令前缀](https://nonebot.dev/docs/appendices/config#command-start-和-command-separator) (默认为`/`)，可自行设置为空**

```
@机器人 remake/liferestart/人生重开/人生重来
```


#### 示例：

<div align="left">
  <img src="https://s2.loli.net/2023/08/02/25YjUFKwvnWisNr.jpg" width="400" />
  <img src="https://s2.loli.net/2023/08/02/b4L7WvnAyHeYUPZ.jpg" width="400" />
</div>


### 特别感谢

- [VickScarlet/lifeRestart](https://github.com/VickScarlet/lifeRestart) やり直すんだ。そして、次はうまくやる。

- [cc004/lifeRestart-py](https://github.com/cc004/lifeRestart-py) lifeRestart game in python

- [DaiShengSheng/lifeRestart_bot](https://github.com/DaiShengSheng/lifeRestart_bot) 适用于HoshinoBot下的人生重来模拟器插件
