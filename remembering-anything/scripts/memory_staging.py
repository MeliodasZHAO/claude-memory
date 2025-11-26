#!/usr/bin/env python3
"""
Memory Staging Area - 记忆暂存区

对话过程中临时存储待提交的记忆，对话结束时统一提交。

使用方式：
    # 添加到暂存区（全局记忆）
    python memory_staging.py add --type fact --content "住在北京"
    python memory_staging.py add --type preference --content "喜欢玩英雄联盟"
    python memory_staging.py add --type experience --content "最近在学 Python"

    # 添加项目记忆
    python memory_staging.py add --type task --project AnyMem --content "实现负面反馈机制"
    python memory_staging.py add --type completed --project AnyMem --content "提示词优化"
    python memory_staging.py add --type decision --project AnyMem --content "使用 React 而非 Vue"
    python memory_staging.py add --type pitfall --project AnyMem --content "dayjs 时区问题"

    # 查看暂存区
    python memory_staging.py list

    # 提交记忆（写入正式记忆文件）
    python memory_staging.py commit

    # 清空暂存区（不提交）
    python memory_staging.py clear
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# 路径配置
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
USER_DATA_DIR = SKILL_DIR / "user-data"
STAGING_FILE = USER_DATA_DIR / "memory" / ".staging.json"
PROJECTS_DIR = USER_DATA_DIR / "memory" / "projects"

# 确保目录存在
(USER_DATA_DIR / "memory").mkdir(parents=True, exist_ok=True)
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

# 类型到类别的默认映射
DEFAULT_CATEGORIES = {
    "fact": "general",
    "preference": "general",
    "experience": "activity"
}

# 全局记忆类型
GLOBAL_TYPES = ["fact", "preference", "experience"]

# 项目记忆类型
PROJECT_TYPES = ["task", "completed", "decision", "pitfall"]


def load_staging() -> List[Dict]:
    """加载暂存区数据"""
    if not STAGING_FILE.exists():
        return []
    try:
        with open(STAGING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_staging(items: List[Dict]):
    """保存暂存区数据"""
    with open(STAGING_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def add_to_staging(
    mem_type: str,
    content: str,
    category: Optional[str] = None,
    tags: Optional[List[str]] = None,
    project: Optional[str] = None,
    priority: Optional[str] = None
) -> Dict:
    """
    添加记忆到暂存区

    Args:
        mem_type: 记忆类型
            - 全局: fact, preference, experience
            - 项目: task, completed, decision, pitfall
        content: 记忆内容
        category: 可选的类别
        tags: 可选的标签列表
        project: 项目名（项目记忆必填）
        priority: 任务优先级 (high/medium/low/none，仅 task 类型)

    Returns:
        添加的条目
    """
    items = load_staging()

    # 检查重复（同项目同类型同内容视为重复）
    for item in items:
        if (item["content"].strip().lower() == content.strip().lower() and
            item["type"] == mem_type and
            item.get("project") == project):
            return item  # 已存在，直接返回

    entry = {
        "type": mem_type,
        "content": content,
        "category": category or DEFAULT_CATEGORIES.get(mem_type, "general"),
        "tags": tags or [],
        "added_at": datetime.now().isoformat(),
        "source": "conversation"
    }

    # 项目记忆附加字段
    if project:
        entry["project"] = project
    if priority and mem_type == "task":
        entry["priority"] = priority

    items.append(entry)
    save_staging(items)
    return entry


def list_staging() -> List[Dict]:
    """列出暂存区所有条目"""
    return load_staging()


def clear_staging():
    """清空暂存区"""
    save_staging([])


def _commit_project_item(item: Dict) -> None:
    """提交单个项目记忆"""
    import uuid

    project = item["project"]
    mem_type = item["type"]
    content = item["content"]

    # 确保项目目录存在
    project_dir = PROJECTS_DIR / project
    project_dir.mkdir(parents=True, exist_ok=True)

    # 根据类型确定目标文件
    if mem_type == "task":
        target_file = project_dir / "tasks.json"
        entry_id = f"task_{uuid.uuid4().hex[:3]}"
        entry = {
            "id": entry_id,
            "title": content,
            "description": "",
            "priority": item.get("priority", "medium"),
            "status": "pending",
            "created": datetime.now().isoformat(),
            "category": item.get("category", "general")
        }
    elif mem_type == "completed":
        target_file = project_dir / "completed.json"
        entry_id = f"done_{uuid.uuid4().hex[:3]}"
        entry = {
            "id": entry_id,
            "title": content,
            "description": "",
            "completed": datetime.now().strftime("%Y-%m-%d"),
            "category": item.get("category", "general")
        }
    elif mem_type == "decision":
        target_file = project_dir / "decisions.json"
        entry_id = f"dec_{uuid.uuid4().hex[:3]}"
        entry = {
            "id": entry_id,
            "decision": content,
            "reason": "",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "category": item.get("category", "architecture")
        }
    elif mem_type == "pitfall":
        target_file = project_dir / "pitfalls.json"
        entry_id = f"pit_{uuid.uuid4().hex[:3]}"
        entry = {
            "id": entry_id,
            "issue": content,
            "solution": "",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "category": item.get("category", "general")
        }
    else:
        raise ValueError(f"Unknown project memory type: {mem_type}")

    # 加载现有数据
    if target_file.exists():
        with open(target_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    # 添加新条目
    data[entry_id] = entry

    # 保存
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def commit_staging() -> Dict:
    """
    提交暂存区的所有记忆到正式记忆文件

    Returns:
        提交结果统计
    """
    items = load_staging()
    if not items:
        return {"committed": 0, "message": "暂存区为空"}

    # 导入 MemoryManager（仅用于全局记忆）
    sys.path.insert(0, str(SCRIPT_DIR))
    from memory_manager import MemoryManager

    mm = MemoryManager()

    results = {
        "committed": 0,
        "facts": 0,
        "preferences": 0,
        "experiences": 0,
        "project_items": 0,
        "errors": []
    }

    for item in items:
        try:
            mem_type = item["type"]
            content = item["content"]
            category = item.get("category", "general")
            tags = item.get("tags", [])
            source = item.get("source", "conversation")

            # 项目记忆
            if mem_type in PROJECT_TYPES:
                if not item.get("project"):
                    raise ValueError("项目记忆必须指定 project 参数")
                _commit_project_item(item)
                results["project_items"] += 1

            # 全局记忆
            elif mem_type == "fact":
                mm.add_fact(
                    content=content,
                    category=category,
                    source=source,
                    tags=tags
                )
                results["facts"] += 1

            elif mem_type == "preference":
                mm.add_preference(
                    content=content,
                    category=category,
                    source=source,
                    tags=tags
                )
                results["preferences"] += 1

            elif mem_type == "experience":
                mm.add_experience(
                    content=content,
                    category=category,
                    source=source,
                    tags=tags
                )
                results["experiences"] += 1

            results["committed"] += 1

        except Exception as e:
            results["errors"].append(f"[{item['type']}] {item['content']}: {str(e)}")

    # 清空暂存区
    clear_staging()

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Memory Staging Area - 记忆暂存区管理',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  全局记忆:
    python memory_staging.py add --type fact --content "住在北京"
    python memory_staging.py add --type preference --content "喜欢喝咖啡"
    python memory_staging.py add --type experience --content "最近在学 Python"

  项目记忆:
    python memory_staging.py add --type task --project AnyMem --content "实现负面反馈"
    python memory_staging.py add --type task --project AnyMem --content "紧急bug" --priority high
    python memory_staging.py add --type completed --project AnyMem --content "提示词优化"
    python memory_staging.py add --type decision --project AnyMem --content "使用React"
    python memory_staging.py add --type pitfall --project AnyMem --content "dayjs时区问题"

  查看/提交:
    python memory_staging.py list
    python memory_staging.py commit
    python memory_staging.py clear
        """
    )

    parser.add_argument(
        'command',
        choices=['add', 'list', 'commit', 'clear', 'count'],
        help='操作命令'
    )
    parser.add_argument(
        '--type', '-t',
        choices=GLOBAL_TYPES + PROJECT_TYPES,
        help='记忆类型 (全局: fact/preference/experience, 项目: task/completed/decision/pitfall)'
    )
    parser.add_argument(
        '--content', '-c',
        help='记忆内容'
    )
    parser.add_argument(
        '--project', '-p',
        help='项目名（项目记忆必填）'
    )
    parser.add_argument(
        '--priority',
        choices=['high', 'medium', 'low', 'none'],
        default='medium',
        help='任务优先级（仅 task 类型有效）'
    )
    parser.add_argument(
        '--category',
        help='记忆类别 (可选)'
    )
    parser.add_argument(
        '--tags',
        help='标签，逗号分隔 (可选)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='以 JSON 格式输出'
    )

    args = parser.parse_args()

    if args.command == 'add':
        if not args.type or not args.content:
            print("错误: add 命令需要 --type 和 --content 参数")
            sys.exit(1)

        # 项目记忆必须指定项目名
        if args.type in PROJECT_TYPES and not args.project:
            print(f"错误: {args.type} 类型是项目记忆，必须指定 --project 参数")
            sys.exit(1)

        # 全局记忆不应指定项目名
        if args.type in GLOBAL_TYPES and args.project:
            print(f"警告: {args.type} 是全局记忆类型，--project 参数将被忽略")

        tags = args.tags.split(',') if args.tags else None
        entry = add_to_staging(
            mem_type=args.type,
            content=args.content,
            category=args.category,
            tags=tags,
            project=args.project if args.type in PROJECT_TYPES else None,
            priority=args.priority if args.type == "task" else None
        )

        if args.json:
            print(json.dumps(entry, ensure_ascii=False))
        else:
            if args.project:
                print(f"[+] 已添加到暂存区: [{entry['type']}@{args.project}] {entry['content']}")
            else:
                print(f"[+] 已添加到暂存区: [{entry['type']}] {entry['content']}")

    elif args.command == 'list':
        items = list_staging()

        if args.json:
            print(json.dumps(items, ensure_ascii=False, indent=2))
        else:
            if not items:
                print("暂存区为空")
            else:
                print(f"\n暂存区记忆 ({len(items)} 条):\n")
                for i, item in enumerate(items, 1):
                    type_icon = {
                        "fact": "F", "preference": "P", "experience": "E",
                        "task": "T", "completed": "D", "decision": "A", "pitfall": "!"
                    }.get(item["type"], "?")

                    # 显示项目名
                    if item.get("project"):
                        print(f"  {i}. [{type_icon}@{item['project']}] {item['content']}")
                    else:
                        print(f"  {i}. [{type_icon}] {item['content']}")

                    # 显示额外信息
                    if item.get("category") and item.get("category") != "general":
                        print(f"      类别: {item['category']}")
                    if item.get("priority") and item["type"] == "task":
                        print(f"      优先级: {item['priority']}")
                print()

    elif args.command == 'commit':
        result = commit_staging()

        if args.json:
            print(json.dumps(result, ensure_ascii=False))
        else:
            if result["committed"] == 0:
                print("暂存区为空，无需提交")
            else:
                print(f"\n[v] 已提交 {result['committed']} 条记忆:")
                if result["facts"]:
                    print(f"    - 事实: {result['facts']} 条")
                if result["preferences"]:
                    print(f"    - 偏好: {result['preferences']} 条")
                if result["experiences"]:
                    print(f"    - 经历: {result['experiences']} 条")
                if result["project_items"]:
                    print(f"    - 项目记忆: {result['project_items']} 条")

                if result["errors"]:
                    print(f"\n[!] 错误 ({len(result['errors'])} 条):")
                    for err in result["errors"]:
                        print(f"    - {err}")
                print()

    elif args.command == 'clear':
        clear_staging()
        if args.json:
            print(json.dumps({"cleared": True}))
        else:
            print("[x] 暂存区已清空")

    elif args.command == 'count':
        items = list_staging()
        if args.json:
            print(json.dumps({"count": len(items)}))
        else:
            print(len(items))


if __name__ == "__main__":
    main()
