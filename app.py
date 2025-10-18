"""
人生重开模拟器 HTTP API 版本
提供不同的路由返回不同的PNG结果
"""
import os
import random
import traceback
from io import BytesIO
from typing import Optional

# 设置环境变量，告诉 nonebot_plugin_remake 跳过 NoneBot 初始化
os.environ["SKIP_NONEBOT_INIT"] = "1"

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator

from nonebot_plugin_remake.drawer import draw_life, save_png
from nonebot_plugin_remake.life import Life
from nonebot_plugin_remake.property import Summary

app = FastAPI(
    title="人生重开模拟器 API",
    description="通过不同路由生成不同的人生重开结果图片",
    version="1.0.0",
)


class CustomLifeRequest(BaseModel):
    """自定义人生请求"""

    talent_ids: list[int] = Field(
        ..., min_length=3, max_length=3, description="选择的3个天赋ID（0-9）"
    )
    chr: int = Field(..., ge=0, le=10, description="颜值（0-10）")
    int_val: int = Field(..., ge=0, le=10, description="智力（0-10）", alias="int")
    str_val: int = Field(..., ge=0, le=10, description="体质（0-10）", alias="str")
    mny: int = Field(..., ge=0, le=10, description="家境（0-10）")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("talent_ids")
    @classmethod
    def validate_talent_ids(cls, v):
        if len(set(v)) != 3:
            raise ValueError("天赋ID不能重复")
        if any(tid < 0 or tid >= 10 for tid in v):
            raise ValueError("天赋ID必须在0-9之间")
        return v


def create_life_image(
    talents,
    init_prop,
    results,
    summary,
) -> BytesIO:
    """创建人生图片(PNG)"""
    return save_png(draw_life(talents, init_prop, results, summary))


def run_life_simulation(
    talent_ids: Optional[list[int]] = None,
    chr: Optional[int] = None,
    int_val: Optional[int] = None,
    str_val: Optional[int] = None,
    mny: Optional[int] = None,
    preselected_talents: Optional[list] = None,
) -> BytesIO:
    """
    运行人生模拟
    如果参数为None，则随机生成
    """
    try:
        life = Life()
        life.load()

        # 选择天赋
        if preselected_talents is not None:
            talents_selected = preselected_talents
        else:
            # 随机生成10个天赋供选择
            all_talents = life.rand_talents(10)
            if talent_ids is None:
                # 随机选择3个不冲突的天赋
                while True:
                    nums = random.sample(range(10), 3)
                    nums.sort()
                    talents_selected = [all_talents[n] for n in nums]
                    # 检查天赋冲突
                    has_conflict = False
                    for i, t1 in enumerate(talents_selected):
                        for t2 in talents_selected[i + 1 :]:
                            if t1.exclusive_with(t2):
                                has_conflict = True
                                break
                        if has_conflict:
                            break
                    if not has_conflict:
                        break
            else:
                talents_selected = [all_talents[i] for i in talent_ids]
                # 检查天赋冲突
                for i, t1 in enumerate(talents_selected):
                    for t2 in talents_selected[i + 1 :]:
                        if t1.exclusive_with(t2):
                            raise ValueError(
                                f'天赋"{t1.name}"和"{t2.name}"不能同时拥有'
                            )

        life.set_talents(talents_selected)
        total_prop = life.total_property()

        # 分配属性
        if chr is None or int_val is None or str_val is None or mny is None:
            # 随机分配属性
            half_prop1 = int(total_prop / 2)
            half_prop2 = total_prop - half_prop1
            num1 = random.randint(0, half_prop1)
            num2 = random.randint(0, half_prop2)
            nums = [num1, num2, half_prop1 - num1, half_prop2 - num2]
            random.shuffle(nums)
            chr, int_val, str_val, mny = nums
        else:
            # 验证属性总和
            if chr + int_val + str_val + mny != total_prop:
                raise ValueError(
                    f"属性之和必须为{total_prop}，当前为{chr + int_val + str_val + mny}"
                )

        prop = {"CHR": chr, "INT": int_val, "STR": str_val, "MNY": mny}
        life.apply_property(prop)

        # 运行人生模拟
        init_prop = life.get_property()
        results = list(life.run())
        summary = life.gen_summary()

        # 生成图片
        img = create_life_image(talents_selected, init_prop, results, summary)
        return img

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"人生重开失败: {str(e)}")


@app.get("/", tags=["信息"])
async def root():
    """API根路径"""
    return {
        "name": "人生重开模拟器 API",
        "version": "1.0.0",
        "routes": {
            "/random": "完全随机的人生（随机天赋和属性）",
            "/custom": "自定义天赋和属性的人生（POST请求）",
            "/talents-info": "获取可用天赋列表",
        },
    }


@app.get("/random", tags=["人生模拟"], response_class=StreamingResponse)
async def random_life():
    """
    完全随机的人生
    随机选择天赋和属性，返回人生重开结果图片
    """
    img = run_life_simulation()
    img.seek(0)
    return StreamingResponse(img, media_type="image/png")


@app.post("/custom", tags=["人生模拟"], response_class=StreamingResponse)
async def custom_life(request: CustomLifeRequest):
    """
    自定义人生
    根据指定的天赋和属性，返回人生重开结果图片

    参数:
    - talent_ids: 选择的3个天赋全局ID（来自数据集），可先调用 /talents-info 获取示例
    - chr: 颜值（0-10）
    - int: 智力（0-10）
    - str: 体质（0-10）
    - mny: 家境（0-10）

    注意：属性总和必须等于天赋提供的总属性点
    """
    # 根据全局ID查找天赋
    life_lookup = Life()
    life_lookup.load()
    id_map = {}
    for grade_list in life_lookup.talent.talent_dict.values():
        for t in grade_list:
            id_map[t.id] = t

    try:
        talents_selected = [id_map[tid] for tid in request.talent_ids]
    except KeyError:
        raise HTTPException(status_code=400, detail="存在无效的天赋ID")

    # 冲突检查
    for i, t1 in enumerate(talents_selected):
        for t2 in talents_selected[i + 1 :]:
            if t1.exclusive_with(t2):
                raise HTTPException(status_code=400, detail=f'天赋"{t1.name}"和"{t2.name}"不能同时拥有')

    img = run_life_simulation(
        preselected_talents=talents_selected,
        chr=request.chr,
        int_val=request.int_val,
        str_val=request.str_val,
        mny=request.mny,
    )
    img.seek(0)
    return StreamingResponse(img, media_type="image/png")


@app.get("/random-talents", tags=["人生模拟"], response_class=StreamingResponse)
async def random_talents_life(
    chr: int = 5, int_val: int = 5, str_val: int = 5, mny: int = 5
):
    """
    随机天赋，固定属性
    随机选择天赋，但使用指定的属性值

    参数:
    - chr: 颜值（0-10）
    - int: 智力（0-10）
    - str: 体质（0-10）
    - mny: 家境（0-10）

    注意：属性总和可能会被调整以匹配天赋提供的总属性点
    """
    # 先随机选择天赋，然后根据总属性点调整
    life = Life()
    life.load()
    all_talents = life.rand_talents(10)

    # 随机选择3个不冲突的天赋
    while True:
        nums = random.sample(range(10), 3)
        nums.sort()
        talents_selected = [all_talents[n] for n in nums]
        has_conflict = False
        for i, t1 in enumerate(talents_selected):
            for t2 in talents_selected[i + 1 :]:
                if t1.exclusive_with(t2):
                    has_conflict = True
                    break
            if has_conflict:
                break
        if not has_conflict:
            break

    life.set_talents(talents_selected)
    total_prop = life.total_property()

    # 按比例调整属性
    current_total = chr + int_val + str_val + mny
    if current_total != total_prop:
        ratio = total_prop / current_total
        chr = int(chr * ratio)
        int_val = int(int_val * ratio)
        str_val = int(str_val * ratio)
        mny = total_prop - chr - int_val - str_val

    img = run_life_simulation(preselected_talents=talents_selected, chr=chr, int_val=int_val, str_val=str_val, mny=mny)
    img.seek(0)
    return StreamingResponse(img, media_type="image/png")


@app.get("/random-attributes", tags=["人生模拟"], response_class=StreamingResponse)
async def random_attributes_life(talent_ids: list[int]):
    """
    固定天赋，随机属性
    使用指定的天赋（使用全局天赋ID），但随机分配属性

    参数:
    - talent_ids: 选择的3个天赋全局ID（来自数据集），例如: ?talent_ids=101&talent_ids=205&talent_ids=309
    """
    if len(talent_ids) != 3:
        raise HTTPException(status_code=400, detail="必须选择3个天赋")
    if len(set(talent_ids)) != 3:
        raise HTTPException(status_code=400, detail="天赋ID不能重复")

    # 根据全局ID查找天赋
    life_lookup = Life()
    life_lookup.load()
    id_map = {}
    for grade_list in life_lookup.talent.talent_dict.values():
        for t in grade_list:
            id_map[t.id] = t

    try:
        talents_selected = [id_map[tid] for tid in talent_ids]
    except KeyError:
        raise HTTPException(status_code=400, detail="存在无效的天赋ID")

    # 冲突检查
    for i, t1 in enumerate(talents_selected):
        for t2 in talents_selected[i + 1 :]:
            if t1.exclusive_with(t2):
                raise HTTPException(status_code=400, detail=f'天赋"{t1.name}"和"{t2.name}"不能同时拥有')

    img = run_life_simulation(preselected_talents=talents_selected)
    img.seek(0)
    return StreamingResponse(img, media_type="image/png")


@app.get("/talents-info", tags=["信息"])
async def talents_info():
    """
    获取一组随机天赋信息（示例）
    提示：自定义接口使用的是全局天赋ID（talent.id）
    """
    try:
        life = Life()
        life.load()
        talents = life.rand_talents(10)

        talents_data = []
        for idx, t in enumerate(talents):
            talents_data.append(
                {
                    "idx": idx,          # 在本次列表中的位置（仅展示用途）
                    "id": t.id,          # 全局天赋ID（用于 /custom 与 /random-attributes）
                    "name": t.name,
                    "description": t.description,
                    "grade": t.grade,
                }
            )

        return {
            "talents": talents_data,
            "note": "注意：请使用返回的全局天赋ID(id) 调用 /custom 或 /random-attributes",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取天赋信息失败: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
