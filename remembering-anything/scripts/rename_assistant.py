#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 助手改名工具 - 安全地修改 AI 名字

功能：
1. 修改 SKILL.md 中的名字
2. 修改 CLAUDE.md 中的名字（智能检测自定义内容）
3. 修改 ai-persona.md 中的名字
4. 支持备份和回滚
5. 支持 dry-run 预览

使用示例：
  python rename_assistant.py --new-name 小白
  python rename_assistant.py --new-name 阿尔法 --dry-run
  python rename_assistant.py --rollback
"""

import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
import re

# 路径配置
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
USER_HOME = Path.home()

# 目标文件列表
TARGET_FILES = {
    "skill": SKILL_DIR / "SKILL.md",
    "ai_persona": SKILL_DIR / "user-data" / "config" / "ai-persona.md",
    "claude_md": USER_HOME / ".claude" / "CLAUDE.md",
}

BACKUP_DIR = SKILL_DIR / "user-data" / "backups" / "rename"


def get_current_name() -> str:
    """从 SKILL.md 获取当前 AI 名字"""
    skill_file = TARGET_FILES["skill"]
    if not skill_file.exists():
        return "夏弥"

    content = skill_file.read_text(encoding="utf-8")
    match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "夏弥"


def is_valid_name(name: str) -> bool:
    """检查名字是否合法（中英文、数字、空格）"""
    if not name or len(name) > 20:
        return False
    # 允许中文、英文、数字、空格
    return bool(re.match(r"^[\u4e00-\u9fa5a-zA-Z0-9\s]+$", name))


def create_backup(old_name: str) -> Path:
    """创建备份"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"backup_{old_name}_{timestamp}"
    backup_path.mkdir(parents=True, exist_ok=True)

    backup_info = {
        "timestamp": timestamp,
        "old_name": old_name,
        "files": []
    }

    # 备份所有目标文件
    for key, file_path in TARGET_FILES.items():
        if file_path.exists():
            backup_file = backup_path / f"{key}.md"
            shutil.copy2(file_path, backup_file)
            backup_info["files"].append({
                "key": key,
                "path": str(file_path),
                "backup": str(backup_file)
            })

    # 保存备份信息
    info_file = backup_path / "backup_info.json"
    info_file.write_text(json.dumps(backup_info, ensure_ascii=False, indent=2), encoding="utf-8")

    return backup_path


def is_default_claude_md(content: str) -> bool:
    """
    检测 CLAUDE.md 是否为默认模板
    如果包含其他 skill 的配置或大量自定义内容，返回 False
    """
    # 简单启发式：检查是否包含其他标记性内容
    custom_markers = [
        "## 自定义规则",
        "## Custom Rules",
        "project_id:",
        "## 其他 Skill",
    ]

    for marker in custom_markers:
        if marker in content:
            return False

    # 检查行数：如果超过默认模板太多，可能有自定义
    lines = content.split("\n")
    if len(lines) > 150:  # 默认模板约 104 行
        return False

    return True


def safe_replace_name(file_path: Path, old_name: str, new_name: str, is_claude_md: bool = False) -> list:
    """
    安全替换名字，返回改动列表

    Args:
        file_path: 文件路径
        old_name: 旧名字
        new_name: 新名字
        is_claude_md: 是否为 CLAUDE.md（需要特殊处理）

    Returns:
        改动列表 [{"line": 行号, "old": 旧内容, "new": 新内容}]
    """
    if not file_path.exists():
        return []

    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    changes = []

    # 如果是 CLAUDE.md 且有自定义内容，只改关键行
    if is_claude_md and not is_default_claude_md(content):
        # 只替换包含旧名字的行（精确匹配）
        patterns = [
            (rf'你是\*\*{re.escape(old_name)}\*\*', f'你是**{new_name}**'),
            (rf'"{re.escape(old_name)}"', f'"{new_name}"'),
            (rf"'{re.escape(old_name)}'", f"'{new_name}'"),
            (rf'「{re.escape(old_name)}」', f'「{new_name}」'),
        ]
    else:
        # 完整替换（所有出现的地方）
        patterns = [
            (re.escape(old_name), new_name),
        ]

    new_lines = []
    for i, line in enumerate(lines):
        new_line = line
        for pattern, replacement in patterns:
            if re.search(pattern, line):
                new_line = re.sub(pattern, replacement, line)
                if new_line != line:
                    changes.append({
                        "line": i + 1,
                        "old": line,
                        "new": new_line
                    })
        new_lines.append(new_line)

    return changes, "\n".join(new_lines)


def show_changes(changes_dict: dict):
    """显示改动预览"""
    if not any(changes_dict.values()):
        print("没有需要修改的内容")
        return

    for file_key, changes in changes_dict.items():
        if not changes:
            continue

        file_path = TARGET_FILES[file_key]
        print(f"\n【{file_path}】")
        for change in changes:
            print(f"  行 {change['line']}:")
            print(f"    - {change['old']}")
            print(f"    + {change['new']}")


def apply_changes(changes_dict: dict, new_contents: dict):
    """应用改动"""
    for file_key, new_content in new_contents.items():
        file_path = TARGET_FILES[file_key]
        if new_content:
            file_path.write_text(new_content, encoding="utf-8")
            print(f"✓ {file_path.name} 更新完成")


def rollback(backup_path: Path):
    """回滚到备份"""
    info_file = backup_path / "backup_info.json"
    if not info_file.exists():
        print(f"错误：备份信息文件不存在 {info_file}")
        return False

    backup_info = json.loads(info_file.read_text(encoding="utf-8"))

    print(f"正在回滚到备份：{backup_info['timestamp']}")
    print(f"恢复名字：{backup_info['old_name']}")

    for file_info in backup_info["files"]:
        src = Path(file_info["backup"])
        dst = Path(file_info["path"])
        if src.exists():
            shutil.copy2(src, dst)
            print(f"✓ 已恢复 {dst.name}")
        else:
            print(f"⚠ 备份文件不存在：{src}")

    return True


def list_backups():
    """列出所有备份"""
    if not BACKUP_DIR.exists():
        print("没有备份记录")
        return []

    backups = []
    for backup_path in sorted(BACKUP_DIR.iterdir(), reverse=True):
        info_file = backup_path / "backup_info.json"
        if info_file.exists():
            info = json.loads(info_file.read_text(encoding="utf-8"))
            backups.append({
                "path": backup_path,
                "timestamp": info["timestamp"],
                "old_name": info["old_name"]
            })

    if not backups:
        print("没有备份记录")
        return []

    print("可用备份：")
    for i, backup in enumerate(backups):
        print(f"  {i + 1}. {backup['timestamp']} - {backup['old_name']}")

    return backups


def main():
    # 设置 UTF-8 编码避免 Windows 终端乱码
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    parser = argparse.ArgumentParser(description="安全地修改 AI 助手名字")
    parser.add_argument("--new-name", help="新名字")
    parser.add_argument("--dry-run", action="store_true", help="预览改动，不实际执行")
    parser.add_argument("--rollback", action="store_true", help="回滚到最近的备份")
    parser.add_argument("--list-backups", action="store_true", help="列出所有备份")

    args = parser.parse_args()

    # 列出备份
    if args.list_backups:
        list_backups()
        return

    # 回滚
    if args.rollback:
        backups = list_backups()
        if not backups:
            return

        choice = input("\n选择要回滚的备份（输入编号，或 q 退出）：").strip()
        if choice.lower() == "q":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(backups):
                rollback(backups[idx]["path"])
            else:
                print("无效的编号")
        except ValueError:
            print("无效的输入")
        return

    # 改名
    if not args.new_name:
        parser.print_help()
        return

    new_name = args.new_name.strip()
    old_name = get_current_name()

    # 检查名字
    if not is_valid_name(new_name):
        print(f"错误：名字不合法（只能包含中英文、数字、空格，长度 1-20）")
        return

    if new_name == old_name:
        print(f"名字没有变化：{old_name}")
        return

    print(f"准备修改 AI 名字：{old_name} → {new_name}")

    # 计算改动
    changes_dict = {}
    new_contents = {}

    for key, file_path in TARGET_FILES.items():
        if not file_path.exists():
            print(f"⚠ 文件不存在，跳过：{file_path}")
            continue

        is_claude = (key == "claude_md")
        changes, new_content = safe_replace_name(file_path, old_name, new_name, is_claude)
        changes_dict[key] = changes
        new_contents[key] = new_content

    # 显示改动
    print("\n改动预览：")
    show_changes(changes_dict)

    if args.dry_run:
        print("\n[Dry Run] 未实际执行改动")
        return

    # 确认
    confirm = input(f"\n确认修改？(y/n): ").strip().lower()
    if confirm != "y":
        print("已取消")
        return

    # 创建备份
    print("\n创建备份...")
    backup_path = create_backup(old_name)
    print(f"✓ 备份已创建：{backup_path}")

    # 应用改动
    print("\n应用改动...")
    apply_changes(changes_dict, new_contents)

    # 刷新缓存
    print("\n刷新缓存...")
    import subprocess
    try:
        subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "activate.py")],
            cwd=str(SKILL_DIR),
            check=True,
            capture_output=True
        )
        print("✓ 缓存已刷新")
    except subprocess.CalledProcessError as e:
        print(f"⚠ 缓存刷新失败：{e}")

    print(f"\n✓ 改名完成！新名字 \"{new_name}\" 已生效，下次呼唤时使用新名字即可。")
    print(f"如需回滚，运行：python {Path(__file__).name} --rollback")


if __name__ == "__main__":
    main()
