#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速加载核心记忆和最近活动

在激活时调用，快速返回必要信息：
- 核心记忆（你是谁、关键关系）
- 最近活动（近7天）
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
    """加载最近活动（只取最近3条）"""
    recent_file = MEMORY_DIR / "recent.json"
    if not recent_file.exists():
        return []

    with open(recent_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("activities", [])[:3]

def check_birthdays_today(core):
    """检查今天是否有生日/纪念日"""
    today = datetime.now().strftime("%m-%d")
    birthdays = []

    # 检查用户生日
    user_birthday = core.get("user", {}).get("birthday", "")
    if user_birthday and user_birthday[5:] == today:
        birthdays.append({"type": "user", "name": "你", "date": user_birthday})

    # 检查宠物生日
    for pet in core.get("pets", []):
        pet_birthday = pet.get("birthday", "")
        if pet_birthday and pet_birthday[5:] == today:
            birthdays.append({
                "type": "pet",
                "name": pet["name"],
                "species": pet.get("type", ""),
                "date": pet_birthday
            })

    # 检查团队成员生日
    team = core.get("team", {})
    for member in team.get("members", []):
        member_birthday = member.get("birthday", "")
        if member_birthday and member_birthday[5:] == today:
            birthdays.append({
                "type": "team_member",
                "name": member["name"],
                "relation": member.get("relation", ""),
                "date": member_birthday
            })

    # 检查团队成立日
    team_formed = team.get("formed", "")
    if team_formed and team_formed[5:] == today:
        years = datetime.now().year - int(team_formed[:4])
        birthdays.append({
            "type": "anniversary",
            "name": "团队成立",
            "years": years,
            "date": team_formed
        })

    # 检查其他团队纪念日
    for anniversary in team.get("anniversaries", []):
        ann_date = anniversary.get("date", "")
        if ann_date == today:
            birthdays.append({
                "type": "anniversary",
                "name": anniversary.get("description", "纪念日"),
                "date": ann_date
            })

    return birthdays

def main():
    """主函数：加载记忆并输出简化摘要"""
    try:
        core = load_core()
        recent = load_recent()
        birthdays = check_birthdays_today(core)

        # 简化输出 - 包含所有关键信息，避免幻觉
        result = {
            "birthdays": [{"name": b["name"], "type": b["type"]} for b in birthdays],
            "recent": recent[0]["content"][:60] + "..." if recent and len(recent[0]["content"]) > 60 else (recent[0]["content"] if recent else ""),
            "user": core.get("user", {}),
            "pets": [{"name": p["name"], "type": p["type"], "breed": p.get("breed", ""), "color": p.get("color", ""), "birthday": p.get("birthday", "")} for p in core.get("pets", [])],
            "team": {"formed": core.get("team", {}).get("formed", ""), "members": [{"name": m["name"], "relation": m.get("relation", ""), "birthday": m.get("birthday", "")} for m in core.get("team", {}).get("members", [])]},
            "preferences": core.get("preferences", {})
        }

        # 写入缓存文件，避免终端编码问题
        cache_file = SKILL_DIR / "user-data" / "memory" / ".quick_load_cache.json"
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        # 只输出状态
        print("ok")

    except Exception as e:
        # 出错时返回空结果
        print(json.dumps({"core": {}, "recent": [], "birthdays": [], "error": str(e)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
