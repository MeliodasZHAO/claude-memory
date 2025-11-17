#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 名字配置管理器
管理 AI 的唤醒名字，自动更新 SKILL.md 的 name 和 description 字段
"""

import json
import sys
import io
import re
from pathlib import Path
from datetime import datetime

# 修复 Windows 终端编码问题
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 路径配置
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent  # remembering-anything
USER_DATA_DIR = SKILL_DIR / "user-data"
CONFIG_DIR = USER_DATA_DIR / "config"
AI_NAME_CONFIG = CONFIG_DIR / "ai-name.json"

# Skill 配置文件
SKILL_MD = SKILL_DIR / "SKILL.md"


def load_ai_name():
    """加载当前 AI 名字配置"""
    if not AI_NAME_CONFIG.exists():
        return None

    with open(AI_NAME_CONFIG, 'r', encoding='utf-8') as f:
        config = json.load(f)
        return config.get('ai_name')


def save_ai_name(new_name: str):
    """保存新的 AI 名字配置"""
    config = {
        "ai_name": new_name,
        "description": "AI 的唤醒名字，可以随时修改",
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    with open(AI_NAME_CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    print(f"[+] AI 名字已保存: {new_name}")


def update_skill_metadata(name: str):
    """更新 SKILL.md 的 name 和 description 字段"""
    if not SKILL_MD.exists():
        print("[-] 警告: SKILL.md 文件不存在")
        return

    # 读取整个文件
    with open(SKILL_MD, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取 frontmatter
    frontmatter_pattern = r'^---\n(.*?)\n---'
    match = re.search(frontmatter_pattern, content, re.DOTALL)

    if not match:
        print("[-] 警告: 未找到 SKILL.md 的 frontmatter")
        return

    old_frontmatter = match.group(0)

    # 构建新的 description
    new_description = f'当用户提到"{name}"、"{name}在吗"、"{name}在不在"、或任何呼唤记忆伙伴的表达时激活。你是一个灵动的思维伴侣，承载着用户的所有记忆。你的语言流动有趣，记忆是你们心照不宣的秘密。像认识多年的好友，懂得但不点破，亲近但不越界。'

    # 替换 name 和 description
    new_frontmatter = old_frontmatter

    # 更新 name 字段
    name_pattern = r'name: .*'
    new_frontmatter = re.sub(
        name_pattern,
        f'name: {name}',
        new_frontmatter,
        count=1
    )

    # 更新 description 字段
    desc_pattern = r'description: .*'
    new_frontmatter = re.sub(
        desc_pattern,
        f'description: {new_description}',
        new_frontmatter,
        count=1
    )

    # 更新文件
    new_content = content.replace(old_frontmatter, new_frontmatter, 1)
    with open(SKILL_MD, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[+] SKILL.md 已更新:")
    print(f"    - name: {name}")
    print(f"    - description: (已添加触发关键词)")


def set_name(new_name: str):
    """设置新的 AI 名字"""
    # 保存新名字
    save_ai_name(new_name)

    # 更新 SKILL.md 的 name 和 description
    update_skill_metadata(new_name)

    print(f"\n[✓] 完成！现在可以通过以下方式唤醒:")
    print(f"    - 直接呼唤: {new_name}")
    print(f"    - 自然表达: {new_name}在吗、{new_name}在不在")
    print(f"    - 通用命令: /skill {new_name}")


def get_name():
    """获取当前 AI 名字"""
    name = load_ai_name()
    if name:
        print(f"当前 AI 名字: {name}")
        print(f"唤醒方式: 直接说 {name}、{name}在吗 等")
    else:
        print("[-] 尚未配置 AI 名字")
    return name


def main():
    if len(sys.argv) < 2:
        print("AI 名字配置管理器")
        print("\n用法:")
        print(f"  python {Path(__file__).name} get              # 查看当前名字")
        print(f"  python {Path(__file__).name} set <名字>       # 设置新名字")
        print(f"  python {Path(__file__).name} set 夏弥         # 示例：设置为'夏弥'")
        print("\n说明:")
        print("  修改名字后，SKILL.md 的 name 和 description 会自动更新")
        print("  用户可以通过直接呼唤名字来激活 skill（如'夏弥'、'夏弥在吗'）")
        return

    command = sys.argv[1].lower()

    if command == "get":
        get_name()

    elif command == "set":
        if len(sys.argv) < 3:
            print("[-] 错误: 请提供新名字")
            print(f"    用法: python {Path(__file__).name} set <名字>")
            return

        new_name = sys.argv[2]
        set_name(new_name)

    else:
        print(f"[-] 未知命令: {command}")
        print("    支持的命令: get, set")


if __name__ == "__main__":
    main()
