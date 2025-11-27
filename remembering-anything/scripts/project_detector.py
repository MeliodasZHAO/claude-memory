#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目检测模块 - 自动识别当前所在项目

检测优先级：
1. CLAUDE.md 中的 project_id 字段
2. Git remote URL
3. 当前目录名（fallback）
"""

import os
import subprocess
import re
from pathlib import Path


def detect_from_claude_md() -> str | None:
    """从 CLAUDE.md 读取 project_id"""
    cwd = Path.cwd()

    # 尝试 .claude/CLAUDE.md
    claude_md = cwd / ".claude" / "CLAUDE.md"
    if not claude_md.exists():
        # 尝试根目录的 CLAUDE.md
        claude_md = cwd / "CLAUDE.md"

    if not claude_md.exists():
        return None

    try:
        with open(claude_md, "r", encoding="utf-8") as f:
            content = f.read()

        # 匹配 project_id: xxx
        match = re.search(r'project_id:\s*["\']?([^"\'\n]+)["\']?', content, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    except Exception:
        pass

    return None


def detect_from_git_remote() -> str | None:
    """从 git remote 解析项目 ID"""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            timeout=2
        )

        if result.returncode != 0:
            return None

        url = result.stdout.strip()

        # HTTPS 格式: https://github.com/owner/repo.git
        https_match = re.search(r'https?://[^/]+/(.+?)(?:\.git)?$', url)
        if https_match:
            return https_match.group(1)

        # SSH 格式: git@github.com:owner/repo.git
        ssh_match = re.search(r'git@[^:]+:(.+?)(?:\.git)?$', url)
        if ssh_match:
            return ssh_match.group(1)

        return None

    except Exception:
        return None


def detect_from_directory() -> str:
    """使用当前目录名作为 fallback"""
    return Path.cwd().name


def detect_project() -> dict:
    """
    主检测函数

    返回：
    {
        "project_id": "owner/repo" 或 "dir_name",
        "source": "claude_md" | "git_remote" | "directory",
        "cwd": "/absolute/path/to/project"
    }
    """
    cwd = str(Path.cwd())

    # 1. 尝试从 CLAUDE.md 读取
    project_id = detect_from_claude_md()
    if project_id:
        return {
            "project_id": project_id,
            "source": "claude_md",
            "cwd": cwd
        }

    # 2. 尝试从 git remote 解析
    project_id = detect_from_git_remote()
    if project_id:
        return {
            "project_id": project_id,
            "source": "git_remote",
            "cwd": cwd
        }

    # 3. Fallback：使用目录名
    project_id = detect_from_directory()
    return {
        "project_id": project_id,
        "source": "directory",
        "cwd": cwd
    }


def get_project_memory_dir(project_id: str) -> Path:
    """获取项目记忆目录"""
    skill_dir = Path(__file__).parent.parent
    memory_dir = skill_dir / "user-data" / "memory" / "projects"

    # 处理 "/" 转为 "__"
    safe_name = project_id.replace("/", "__")

    return memory_dir / f"{safe_name}.json"


def ensure_project_memory_structure(project_id: str) -> Path:
    """确保项目记忆目录结构存在"""
    memory_file = get_project_memory_dir(project_id)

    # 确保父目录存在
    memory_file.parent.mkdir(parents=True, exist_ok=True)

    # 如果文件不存在，创建空结构
    if not memory_file.exists():
        initial_structure = {
            "name": project_id,
            "description": "",
            "tech_stack": [],
            "current_focus": "",
            "last_active": "",
            "tasks": [],
            "completed": [],
            "decisions": [],
            "pitfalls": []
        }

        import json
        with open(memory_file, "w", encoding="utf-8") as f:
            json.dump(initial_structure, f, ensure_ascii=False, indent=2)

    return memory_file


if __name__ == "__main__":
    # 测试
    result = detect_project()
    print(f"Project ID: {result['project_id']}")
    print(f"Source: {result['source']}")
    print(f"CWD: {result['cwd']}")
