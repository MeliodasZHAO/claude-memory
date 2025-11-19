#!/usr/bin/env python3
"""
路径配置模块 - 统一管理所有路径

开发环境和运行环境使用不同的路径策略：
- 开发环境：指向 ~/.claude/skills/remembering-anything/user-data/
- 运行环境：使用相对路径 ../user-data/
"""

from pathlib import Path
import os


def get_user_data_dir():
    """
    获取 user-data 目录的绝对路径

    策略：
    1. 检查是否在开发环境（存在上层的 claude-memory 目录）
    2. 如果是开发环境，指向运行环境的 user-data
    3. 如果是运行环境，使用相对路径
    """
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent  # remembering-anything/

    # 检查是否在开发环境
    # 开发环境路径: ~/.claude/skills/claude-memory/remembering-anything/scripts/
    # 运行环境路径: ~/.claude/skills/remembering-anything/scripts/
    parent_dir = skill_dir.parent
    is_dev_env = parent_dir.name == "claude-memory"

    if is_dev_env:
        # 开发环境：指向运行环境的 user-data
        # 从 claude-memory/remembering-anything/ 指向 ../../remembering-anything/user-data
        skills_dir = parent_dir.parent  # ~/.claude/skills/
        runtime_skill_dir = skills_dir / "remembering-anything"
        user_data = runtime_skill_dir / "user-data"
        print(f"[开发模式] user-data 路径: {user_data}")
    else:
        # 运行环境：使用相对路径
        user_data = skill_dir / "user-data"
        print(f"[运行模式] user-data 路径: {user_data}")

    # 确保目录存在
    if not user_data.exists():
        print(f"[警告] user-data 目录不存在，正在创建: {user_data}")
        user_data.mkdir(parents=True, exist_ok=True)

    return user_data


def get_memory_dir():
    """获取 memory 目录"""
    return get_user_data_dir() / "memory"


def get_notes_dir():
    """获取 notes 目录"""
    return get_user_data_dir() / "notes"


def get_config_dir():
    """获取 config 目录"""
    return get_user_data_dir() / "config"


def get_summaries_dir():
    """获取 summaries 目录"""
    return get_user_data_dir() / "summaries"


def get_media_dir():
    """获取 media 目录"""
    return get_user_data_dir() / "media"


def get_outputs_dir():
    """获取 outputs 目录"""
    return get_user_data_dir() / "outputs"


def get_backups_dir():
    """获取 backups 目录"""
    return get_user_data_dir() / "backups"


# 测试
if __name__ == "__main__":
    print("=== 路径配置测试 ===\n")
    print(f"user-data: {get_user_data_dir()}")
    print(f"memory:    {get_memory_dir()}")
    print(f"notes:     {get_notes_dir()}")
    print(f"config:    {get_config_dir()}")
    print(f"outputs:   {get_outputs_dir()}")
