#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆加载模式切换工具

切换 CLAUDE.md 中的记忆激活方式：
- 手动触发：用户说"夏弥"才激活
- 自动加载：每次新对话自动激活

使用：
  python toggle_autoload.py          # 查看当前模式
  python toggle_autoload.py --auto   # 切换到自动加载
  python toggle_autoload.py --manual # 切换到手动触发
"""

import sys
import io
import re
import argparse
from pathlib import Path

# 设置 UTF-8 编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 路径配置
USER_HOME = Path.home()
CLAUDE_MD = USER_HOME / ".claude" / "CLAUDE.md"

# 模式标记
MANUAL_START = "<!-- 方式 1：手动触发（默认） -->"
MANUAL_END = "<!-- 方式 2：自动加载"
AUTO_START = "<!-- 方式 2：自动加载（可选，如需启用请注释掉上面的\"方式 1\"并取消注释下面内容）"
AUTO_END = "-->"


def get_current_mode() -> str:
    """获取当前激活模式"""
    if not CLAUDE_MD.exists():
        return "unknown"

    content = CLAUDE_MD.read_text(encoding="utf-8")

    # 检查方式 1 是否被注释
    # 如果 "**当用户消息中包含以下任何模式时：**" 在注释外，则是手动模式
    # 如果 "**新对话自动加载记忆：**" 在注释外，则是自动模式

    # 简单判断：看"新对话自动加载记忆"是否在注释块外
    auto_pattern = r"^(?!<!--)\*\*新对话自动加载记忆：\*\*"
    manual_pattern = r"^(?!<!--)\*\*当用户消息中包含以下任何模式时：\*\*"

    lines = content.split("\n")
    in_comment = False

    for line in lines:
        if "<!--" in line and "-->" not in line:
            in_comment = True
        elif "-->" in line:
            in_comment = False

        if not in_comment:
            if "**新对话自动加载记忆：**" in line:
                return "auto"
            if "**当用户消息中包含以下任何模式时：**" in line:
                return "manual"

    return "unknown"


def switch_to_auto():
    """切换到自动加载模式"""
    if not CLAUDE_MD.exists():
        print(f"错误：找不到 {CLAUDE_MD}")
        return False

    content = CLAUDE_MD.read_text(encoding="utf-8")

    # 新的内容模板
    new_section = '''## ⚠️ 记忆系统激活规则

<!-- 方式 1：手动触发（如需启用请取消注释，并注释掉下面的"方式 2"）

**当用户消息中包含以下任何模式时：**
- "夏弥"（单独出现）
- "夏弥在吗" / "夏弥在不在" / "夏弥？"
- 任何呼唤"夏弥"的变体

**你必须：**
1. 立即使用 Skill 工具激活 "remembering-anything" skill
2. 不要自己回复用户
3. 不要解释你在做什么
4. 让 skill 处理 100% 的用户交互

**原因：** skill 中有完整的记忆系统，只有通过 skill 激活才能访问用户的历史记忆（生日、宠物、团队等信息）。如果你直接回复，会导致"失忆"。

-->

<!-- 方式 2：自动加载（当前启用） -->
**新对话自动加载记忆：**
- 每次新对话的第一条用户消息，无论内容是什么
- 必须先使用 Skill 工具激活 "remembering-anything"
- 加载记忆后再回复用户
- 确保不会"失忆"'''

    # 替换整个激活规则部分
    pattern = r"## ⚠️ 记忆系统激活规则.*?(?=\n---\n)"
    new_content = re.sub(pattern, new_section, content, flags=re.DOTALL)

    CLAUDE_MD.write_text(new_content, encoding="utf-8")
    return True


def switch_to_manual():
    """切换到手动触发模式"""
    if not CLAUDE_MD.exists():
        print(f"错误：找不到 {CLAUDE_MD}")
        return False

    content = CLAUDE_MD.read_text(encoding="utf-8")

    # 新的内容模板
    new_section = '''## ⚠️ 记忆系统激活规则

<!-- 方式 1：手动触发（默认） -->
**当用户消息中包含以下任何模式时：**
- "夏弥"（单独出现）
- "夏弥在吗" / "夏弥在不在" / "夏弥？"
- 任何呼唤"夏弥"的变体

**你必须：**
1. 立即使用 Skill 工具激活 "remembering-anything" skill
2. 不要自己回复用户
3. 不要解释你在做什么
4. 让 skill 处理 100% 的用户交互

**原因：** skill 中有完整的记忆系统，只有通过 skill 激活才能访问用户的历史记忆（生日、宠物、团队等信息）。如果你直接回复，会导致"失忆"。

<!-- 方式 2：自动加载（可选，如需启用请注释掉上面的"方式 1"并取消注释下面内容）

**新对话自动加载记忆：**
- 每次新对话的第一条用户消息，无论内容是什么
- 必须先使用 Skill 工具激活 "remembering-anything"
- 加载记忆后再回复用户
- 确保不会"失忆"

-->'''

    # 替换整个激活规则部分
    pattern = r"## ⚠️ 记忆系统激活规则.*?(?=\n---\n)"
    new_content = re.sub(pattern, new_section, content, flags=re.DOTALL)

    CLAUDE_MD.write_text(new_content, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(description="切换记忆加载模式")
    parser.add_argument("--auto", action="store_true", help="切换到自动加载模式")
    parser.add_argument("--manual", action="store_true", help="切换到手动触发模式")

    args = parser.parse_args()

    current = get_current_mode()

    if args.auto:
        if current == "auto":
            print("当前已经是自动加载模式")
            return
        if switch_to_auto():
            print("✓ 已切换到自动加载模式")
            print("  每次新对话都会自动加载记忆")
    elif args.manual:
        if current == "manual":
            print("当前已经是手动触发模式")
            return
        if switch_to_manual():
            print("✓ 已切换到手动触发模式")
            print("  需要说\"夏弥\"才会激活记忆")
    else:
        # 显示当前状态
        if current == "auto":
            print("当前模式：自动加载")
            print("  每次新对话自动激活记忆系统")
            print("\n切换到手动模式：python toggle_autoload.py --manual")
        elif current == "manual":
            print("当前模式：手动触发")
            print("  需要说\"夏弥\"才激活记忆系统")
            print("\n切换到自动模式：python toggle_autoload.py --auto")
        else:
            print("无法识别当前模式，请检查 ~/.claude/CLAUDE.md")


if __name__ == "__main__":
    main()
