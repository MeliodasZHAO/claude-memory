#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速加载核心记忆和最近活动（改进版）

在激活时调用，快速返回必要信息：
- 核心记忆（你是谁、关键关系）
- 最近活动（按日期排序，优先显示最新的）
- 今天的生日/纪念日

输出 JSON 格式，供 SKILL.md 解析使用
"""

import json
from pathlib import Path
from datetime import datetime

# 获取 skill 目录
SKILL_DIR = Path(__file__).parent.parent
MEMORY_DIR = SKILL_DIR / "user-data" / "memory"

def load_core():
    """加载核心记忆"""
    core_file = MEMORY_DIR / "core.json"
    if not core_file.exists():
        return {}

    with open(core_file, "r", encoding="utf-8") as f:
        return json.load(f)

def load_recent():
    """加载最近活动（按日期排序，取最新的）"""
    recent_file = MEMORY_DIR / "recent.json"
    if not recent_file.exists():
        return []

    with open(recent_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        activities = data.get("activities", [])

        # 按日期降序排序（最新的在前）
        activities.sort(key=lambda x: x.get("date", ""), reverse=True)

        # 只返回最近3条
        return activities[:3]

def check_special_dates_today(core):
    """检查今天是否有重要日期（生日、纪念日、节日等）"""
    today = datetime.now().strftime("%m-%d")
    special_dates = []

    # 检查用户生日
    user_birthday = core.get("user", {}).get("birthday", "")
    if user_birthday and user_birthday[5:] == today:
        special_dates.append({
            "type": "user_birthday",
            "name": "你",
            "date": today
        })

    # 检查宠物生日
    for pet in core.get("pets", []):
        pet_birthday = pet.get("birthday", "")
        if pet_birthday and pet_birthday[5:] == today:
            years = datetime.now().year - int(pet_birthday[:4]) if len(pet_birthday) >= 4 else None
            special_dates.append({
                "type": "pet_birthday",
                "name": pet["name"],
                "date": today,
                "years": years
            })

    # 检查团队成员生日
    team = core.get("team", {})
    for member in team.get("members", []):
        member_birthday = member.get("birthday", "")
        if member_birthday and member_birthday[5:] == today:
            special_dates.append({
                "type": "team_member_birthday",
                "name": member["name"],
                "date": today
            })

    # 检查团队成立日
    team_formed = team.get("formed", "")
    if team_formed and team_formed[5:] == today:
        years = datetime.now().year - int(team_formed[:4])
        special_dates.append({
            "type": "anniversary",
            "name": "团队成立",
            "years": years,
            "date": today
        })

    # 检查结婚纪念日
    wedding_date = core.get("user", {}).get("wedding_anniversary", "")
    if wedding_date and wedding_date[5:] == today:
        years = datetime.now().year - int(wedding_date[:4])
        special_dates.append({
            "type": "wedding_anniversary",
            "name": "结婚纪念日",
            "years": years,
            "date": today
        })

    # 检查其他纪念日
    for anniversary in core.get("anniversaries", []):
        ann_date = anniversary.get("date", "")
        if ann_date and ann_date[5:] == today:
            years = datetime.now().year - int(ann_date[:4]) if len(ann_date) >= 4 else None
            special_dates.append({
                "type": anniversary.get("type", "anniversary"),
                "name": anniversary.get("name", "纪念日"),
                "years": years,
                "date": today
            })

    return special_dates

def main():
    """主函数：加载记忆并输出简化摘要"""
    try:
        core = load_core()
        recent = load_recent()
        special_dates = check_special_dates_today(core)

        # 构建结果 - 包含所有关键信息
        result = {
            "special_dates": special_dates,
            "recent": recent[0]["content"] if recent else "",
            "recent_date": recent[0]["date"] if recent else "",
            "recent_status": recent[0].get("status", "") if recent else "",
            "user": core.get("user", {}),
            "pets": [
                {
                    "name": p["name"],
                    "type": p["type"],
                    "breed": p.get("breed", ""),
                    "color": p.get("color", ""),
                    "birthday": p.get("birthday", "")
                }
                for p in core.get("pets", [])
            ],
            "team": {
                "formed": core.get("team", {}).get("formed", ""),
                "members": [
                    {
                        "name": m["name"],
                        "relation": m.get("relation", ""),
                        "birthday": m.get("birthday", "")
                    }
                    for m in core.get("team", {}).get("members", [])
                ]
            },
            "preferences": core.get("preferences", {})
        }

        # 写入缓存文件
        cache_file = SKILL_DIR / "user-data" / "memory" / ".quick_load_cache.json"
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        # 只输出状态
        print("ok")

    except Exception as e:
        # 出错时返回错误信息
        print(json.dumps({
            "error": str(e),
            "special_dates": [],
            "recent": "",
            "user": {}
        }, ensure_ascii=False))

if __name__ == "__main__":
    main()