#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速加载记忆系统（支持全局 + 项目记忆）

在激活时调用，快速返回必要信息：
- 全局记忆（你是谁、关键关系、偏好）
- 项目记忆（当前项目的架构、约定、踩坑记录）
- 最近活动（按日期排序）
- 今天的生日/纪念日

输出到缓存文件，供 SKILL.md 解析使用
"""

import json
from pathlib import Path
from datetime import datetime
import sys

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from project_detector import detect_project

# 获取 skill 目录
SKILL_DIR = Path(__file__).parent.parent
MEMORY_DIR = SKILL_DIR / "user-data" / "memory"
PROJECTS_DIR = MEMORY_DIR / "projects"


def load_json_file(file_path: Path) -> dict | list:
    """安全加载 JSON 文件"""
    if not file_path.exists():
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def load_global_memory() -> dict:
    """加载全局记忆（直接在 memory 目录下）"""
    return {
        "facts": load_json_file(MEMORY_DIR / "facts.json"),
        "preferences": load_json_file(MEMORY_DIR / "preferences.json"),
        "experiences": load_json_file(MEMORY_DIR / "experiences.json")
    }


def load_project_memory(project_id: str) -> dict | None:
    """加载项目记忆"""
    # 尝试多种命名方式
    possible_names = [
        project_id,
        project_id.replace("/", "__"),
        project_id.split("/")[-1] if "/" in project_id else project_id
    ]

    project_dir = None
    for name in possible_names:
        candidate = PROJECTS_DIR / name
        if candidate.exists():
            project_dir = candidate
            break

    if not project_dir:
        return None

    return {
        "context": load_json_file(project_dir / "context.json"),
        "tasks": load_json_file(project_dir / "tasks.json"),
        "completed": load_json_file(project_dir / "completed.json"),
        "decisions": load_json_file(project_dir / "decisions.json"),
        "pitfalls": load_json_file(project_dir / "pitfalls.json")
    }


def load_recent() -> list:
    """加载最近活动"""
    recent_file = MEMORY_DIR / "recent.json"
    if not recent_file.exists():
        return []

    data = load_json_file(recent_file)
    activities = data.get("activities", [])
    activities.sort(key=lambda x: x.get("date", ""), reverse=True)
    return activities[:3]


def extract_core_info(global_mem: dict) -> dict:
    """从 global facts 中提取核心信息"""
    facts = global_mem.get("facts", {})
    preferences = global_mem.get("preferences", {})

    core = {"user": {}, "pets": [], "team": {}, "preferences": {}}

    for mem_id, mem in facts.items():
        category = mem.get("category", "")
        metadata = mem.get("metadata", {})

        if category == "personal":
            core["user"] = metadata
        elif category == "pet":
            core["pets"].append(metadata)
        elif category == "team":
            core["team"] = {"formed": metadata.get("formed", ""), "members": metadata.get("members", [])}

    for mem_id, mem in preferences.items():
        category = mem.get("category", "other")
        content = mem.get("content", "")
        if category not in core["preferences"]:
            core["preferences"][category] = []
        core["preferences"][category].append(content)

    return core


def check_special_dates_today(core: dict) -> list:
    """检查今天是否有重要日期"""
    today = datetime.now().strftime("%m-%d")
    special_dates = []

    # 检查用户生日
    user_birthday = core.get("user", {}).get("birthday", "")
    if user_birthday and user_birthday[5:] == today:
        special_dates.append({"type": "user_birthday", "name": "你", "date": today})

    # 检查宠物生日
    for pet in core.get("pets", []):
        pet_birthday = pet.get("birthday", "")
        if pet_birthday and pet_birthday[5:] == today:
            years = datetime.now().year - int(pet_birthday[:4]) if len(pet_birthday) >= 4 else None
            special_dates.append({
                "type": "pet_birthday",
                "name": pet.get("name", "宠物"),
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
                "name": member.get("name", ""),
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

    return special_dates


def format_project_summary(project_mem: dict | None) -> dict:
    """格式化项目记忆（直接返回完整数据，不再压缩）"""
    if not project_mem:
        return {}

    # 直接返回完整的项目记忆，因为通常数据量不大
    return project_mem


def main():
    """主函数：加载记忆并输出简化摘要"""
    try:
        # 1. 检测当前项目
        project_info = detect_project()
        project_id = project_info.get("project_id")
        project_source = project_info.get("source")

        # 2. 加载全局记忆
        global_mem = load_global_memory()
        core = extract_core_info(global_mem)

        # 3. 加载项目记忆（如果在项目中）
        project_mem = None
        if project_id and project_source in ("claude_md", "git_remote"):
            project_mem = load_project_memory(project_id)

        # 4. 加载最近活动
        recent = load_recent()

        # 5. 检查今天的特殊日期
        special_dates = check_special_dates_today(core)

        # 6. 构建结果
        result = {
            "project": {
                "id": project_id,
                "source": project_source,
                "has_memory": project_mem is not None
            },
            "special_dates": special_dates,
            "recent": recent[0]["content"] if recent else "",
            "recent_date": recent[0]["date"] if recent else "",
            "recent_status": recent[0].get("status", "") if recent else "",
            "user": core.get("user", {}),
            "pets": core.get("pets", []),
            "team": core.get("team", {}),
            "preferences": core.get("preferences", {}),
            "project_memory": format_project_summary(project_mem) if project_mem else None
        }

        # 7. 写入缓存文件
        cache_file = MEMORY_DIR / ".quick_load_cache.json"
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        # 输出状态
        if project_mem:
            print(f"ok (project: {project_id})")
        else:
            print("ok")

    except Exception as e:
        error_result = {
            "error": str(e),
            "project": None,
            "special_dates": [],
            "recent": "",
            "user": {},
            "pets": [],
            "team": {},
            "preferences": {},
            "project_memory": None
        }
        cache_file = MEMORY_DIR / ".quick_load_cache.json"
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(error_result, f, ensure_ascii=False, indent=2)
        print(f"error: {e}")


if __name__ == "__main__":
    main()
