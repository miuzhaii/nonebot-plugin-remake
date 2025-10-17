import base64
import json
import random
import uuid
from dataclasses import asdict
from io import BytesIO
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .drawer import draw_life, save_jpg
from .life import Life
from .talent import Talent

# 存储游戏会话
game_sessions: dict[str, dict] = {}


def create_web_app() -> FastAPI:
    """创建Web应用"""
    app = FastAPI(title="人生重开模拟器", description="Web版人生重开模拟器")

    # 静态文件目录
    static_dir = Path(__file__).parent / "web_static"
    static_dir.mkdir(exist_ok=True)

    @app.get("/", response_class=HTMLResponse)
    async def index():
        """首页"""
        html_file = Path(__file__).parent / "web_static" / "index.html"
        if html_file.exists():
            return html_file.read_text(encoding="utf-8")
        return """
        <html>
        <head>
            <title>人生重开模拟器</title>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>人生重开模拟器</h1>
            <p>请先生成前端文件</p>
        </body>
        </html>
        """

    @app.get("/api/start")
    async def start_game():
        """开始新游戏"""
        session_id = str(uuid.uuid4())
        life = Life()
        life.load()
        talents = life.rand_talents(10)

        game_sessions[session_id] = {
            "life": life,
            "talents": talents,
            "selected_talents": None,
            "init_prop": None,
            "results": None,
            "summary": None,
        }

        talents_data = [
            {
                "id": i,
                "name": t.name,
                "description": t.description,
                "grade": t.grade,
            }
            for i, t in enumerate(talents)
        ]

        return JSONResponse(
            {
                "session_id": session_id,
                "talents": talents_data,
                "total_property": life.total_property(),
            }
        )

    @app.post("/api/select-talents")
    async def select_talents(data: dict):
        """选择天赋"""
        session_id = data.get("session_id")
        talent_ids = data.get("talent_ids", [])

        if session_id not in game_sessions:
            raise HTTPException(status_code=404, detail="游戏会话不存在")

        session = game_sessions[session_id]
        talents = session["talents"]

        if len(talent_ids) != 3:
            raise HTTPException(status_code=400, detail="必须选择3个天赋")

        try:
            selected_talents = [talents[int(tid)] for tid in talent_ids]
        except (IndexError, ValueError):
            raise HTTPException(status_code=400, detail="无效的天赋ID")

        # 检查天赋冲突
        for i, t1 in enumerate(selected_talents):
            for t2 in selected_talents[i + 1 :]:
                if t1.exclusive_with(t2):
                    raise HTTPException(
                        status_code=400,
                        detail=f'天赋"{t1.name}"和"{t2.name}"不能同时拥有',
                    )

        session["selected_talents"] = selected_talents
        life: Life = session["life"]
        life.set_talents(selected_talents)

        return JSONResponse(
            {"status": "ok", "total_property": life.total_property()}
        )

    @app.post("/api/random-talents")
    async def random_talents(data: dict):
        """随机选择天赋"""
        session_id = data.get("session_id")

        if session_id not in game_sessions:
            raise HTTPException(status_code=404, detail="游戏会话不存在")

        session = game_sessions[session_id]
        talents = session["talents"]

        # 随机选择不冲突的3个天赋
        while True:
            nums = random.sample(range(10), 3)
            nums.sort()
            selected_talents = [talents[n] for n in nums]

            conflict = False
            for i, t1 in enumerate(selected_talents):
                for t2 in selected_talents[i + 1 :]:
                    if t1.exclusive_with(t2):
                        conflict = True
                        break
                if conflict:
                    break

            if not conflict:
                break

        session["selected_talents"] = selected_talents
        life: Life = session["life"]
        life.set_talents(selected_talents)

        return JSONResponse(
            {
                "status": "ok",
                "talent_ids": nums,
                "total_property": life.total_property(),
            }
        )

    @app.post("/api/allocate-property")
    async def allocate_property(data: dict):
        """分配属性点"""
        session_id = data.get("session_id")
        props = data.get("properties", {})

        if session_id not in game_sessions:
            raise HTTPException(status_code=404, detail="游戏会话不存在")

        session = game_sessions[session_id]
        life: Life = session["life"]

        if session["selected_talents"] is None:
            raise HTTPException(status_code=400, detail="请先选择天赋")

        chr_val = props.get("CHR", 0)
        int_val = props.get("INT", 0)
        str_val = props.get("STR", 0)
        mny_val = props.get("MNY", 0)

        total_prop = life.total_property()
        prop_sum = chr_val + int_val + str_val + mny_val

        if prop_sum != total_prop:
            raise HTTPException(
                status_code=400,
                detail=f"属性之和必须为{total_prop}，当前为{prop_sum}",
            )

        if max(chr_val, int_val, str_val, mny_val) > 10:
            raise HTTPException(status_code=400, detail="每个属性不能超过10")

        if min(chr_val, int_val, str_val, mny_val) < 0:
            raise HTTPException(status_code=400, detail="属性不能为负数")

        prop = {"CHR": chr_val, "INT": int_val, "STR": str_val, "MNY": mny_val}
        life.apply_property(prop)

        return JSONResponse({"status": "ok"})

    @app.post("/api/random-property")
    async def random_property(data: dict):
        """随机分配属性点"""
        session_id = data.get("session_id")

        if session_id not in game_sessions:
            raise HTTPException(status_code=404, detail="游戏会话不存在")

        session = game_sessions[session_id]
        life: Life = session["life"]

        if session["selected_talents"] is None:
            raise HTTPException(status_code=400, detail="请先选择天赋")

        total_prop = life.total_property()
        half_prop1 = int(total_prop / 2)
        half_prop2 = total_prop - half_prop1
        num1 = random.randint(0, half_prop1)
        num2 = random.randint(0, half_prop2)
        nums = [num1, num2, half_prop1 - num1, half_prop2 - num2]
        random.shuffle(nums)

        prop = {"CHR": nums[0], "INT": nums[1], "STR": nums[2], "MNY": nums[3]}
        life.apply_property(prop)

        return JSONResponse({"status": "ok", "properties": prop})

    @app.post("/api/run")
    async def run_life(data: dict):
        """运行人生模拟"""
        session_id = data.get("session_id")

        if session_id not in game_sessions:
            raise HTTPException(status_code=404, detail="游戏会话不存在")

        session = game_sessions[session_id]
        life: Life = session["life"]

        if session["selected_talents"] is None:
            raise HTTPException(status_code=400, detail="请先选择天赋")

        init_prop = life.get_property()
        results = list(life.run())
        summary = life.gen_summary()

        session["init_prop"] = init_prop
        session["results"] = results
        session["summary"] = summary

        # 转换结果为可序列化的格式
        results_data = []
        for result in results:
            results_data.append(
                {
                    "property": {
                        "AGE": result.property.AGE,
                        "CHR": result.property.CHR,
                        "INT": result.property.INT,
                        "STR": result.property.STR,
                        "MNY": result.property.MNY,
                        "SPR": result.property.SPR,
                    },
                    "event_log": result.event_log,
                    "talent_log": result.talent_log,
                }
            )

        summary_data = {
            "AGE": summary.AGE,
            "CHR": summary.CHR,
            "INT": summary.INT,
            "STR": summary.STR,
            "MNY": summary.MNY,
            "SPR": summary.SPR,
            "SUM": summary.SUM,
        }

        return JSONResponse(
            {"status": "ok", "results": results_data, "summary": summary_data}
        )

    @app.get("/api/image/{session_id}")
    async def get_life_image(session_id: str):
        """获取人生图片"""
        if session_id not in game_sessions:
            raise HTTPException(status_code=404, detail="游戏会话不存在")

        session = game_sessions[session_id]

        if session["results"] is None:
            raise HTTPException(status_code=400, detail="请先运行人生模拟")

        try:
            img_bytes = save_jpg(
                draw_life(
                    session["selected_talents"],
                    session["init_prop"],
                    session["results"],
                    session["summary"],
                )
            )
            img_base64 = base64.b64encode(img_bytes.getvalue()).decode()
            return JSONResponse({"image": f"data:image/jpeg;base64,{img_base64}"})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"生成图片失败: {str(e)}")

    @app.post("/api/restart")
    async def restart_game(data: dict):
        """重启游戏"""
        session_id = data.get("session_id")

        if session_id in game_sessions:
            del game_sessions[session_id]

        # 创建新会话
        return await start_game()

    return app


# 创建FastAPI应用实例
web_app = create_web_app()
