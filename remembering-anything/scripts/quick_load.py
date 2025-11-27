#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速加载记忆系统（支持全局 + 项目记忆）

在激活时调用，快速返回必要信息：
- 全局记忆（你是谁、关键关系、偏好）
- 项目记忆（当前项目的架构、约定、踩坑记录）
- 最近活动（按日期排序，项目优先）
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
    """加载项目记忆（每个项目一个 json 文件）"""
    # 标准命名：owner/repo -> owner__repo.json
    safe_name = project_id.replace("/", "__")
    standard_path = PROJECTS_DIR / f"{safe_name}.json"

    if standard_path.exists():
        return load_json_file(standard_path)

    return None


def load_recent(project_id: str | None = None) -> list:
    """
    加载最近活动

    优先级：
    1. 当前项目的最近活动（如果有 project 字段匹配）
    2. 全局活动（没有 project 字段的）
    """
    recent_file = MEMORY_DIR / "recent.json"
    if not recent_file.exists():
        return []

    data = load_json_file(recent_file)
    activities = data.get("activities", [])
    activities.sort(key=lambda x: x.get("date", ""), reverse=True)

    if not project_id:
        return activities[:3]

    # 分离：当前项目的活动 vs 全局活动
    project_activities = []
    global_activities = []

    for act in activities:
        act_project = act.get("project")
        if act_project == project_id:
            project_activities.append(act)
        elif act_project is None:
            global_activities.append(act)
        # 其他项目的活动不包含

    # 优先返回当前项目的活动，不够再用全局的补充
    result = project_activities[:3]
    if len(result) < 3:
        result.extend(global_activities[:3 - len(result)])

    return result


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

        # 3. 加载项目记忆（任何有 project_id 的情况都尝试加载）
        project_mem = None
        if project_id:
            project_mem = load_project_memory(project_id)

        # 4. 加载最近活动（优先当前项目的）
        recent = load_recent(project_id)

        # 5. 检查今天的特殊日期
        special_dates = check_special_dates_today(core)

        # 6. 构建结果
        # 确定 recent：项目记忆优先于全局 recent
        recent_content = ""
        recent_date = ""
        recent_status = ""

        if project_mem:
            # 优先用项目的 current_focus
            current_focus = project_mem.get("current_focus", "")
            if current_focus:
                recent_content = current_focus
                recent_date = project_mem.get("last_active", "")
                recent_status = "in_progress"
            else:
                # 没有 current_focus，看最近完成的任务
                completed = project_mem.get("completed", [])
                if completed:
                    latest = completed[-1]  # 最新的在最后
                    recent_content = latest.get("title", "")
                    recent_date = latest.get("date", "")
                    recent_status = "completed"

        # 如果项目没有活动，使用全局 recent
        if not recent_content and recent:
            recent_content = recent[0]["content"]
            recent_date = recent[0]["date"]
            recent_status = recent[0].get("status", "")

        result = {
            "project": {
                "id": project_id,
                "source": project_source,
                "has_memory": project_mem is not None
            },
            "special_dates": special_dates,
            "recent": recent_content,
            "recent_date": recent_date,
            "recent_status": recent_status,
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
