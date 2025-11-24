#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一激活脚本 - 一步完成所有初始化

功能：
1. 检查暂存区并自动提交（确保记忆不丢失）
2. 检查缓存新鲜度（5 分钟内直接使用）
3. 运行 quick_load.py 生成缓存（如果需要）
4. 静默返回
"""

import sys
import os
import time
from pathlib import Path

# 添加脚本目录到路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

# 路径配置
SKILL_DIR = script_dir.parent
CACHE_FILE = SKILL_DIR / "user-data" / "memory" / ".quick_load_cache.json"
STAGING_FILE = SKILL_DIR / "user-data" / "memory" / ".staging.json"

# 缓存有效期（秒）
CACHE_TTL = 300  # 5 分钟


def is_cache_fresh() -> bool:
    """检查缓存是否在有效期内"""
    if not CACHE_FILE.exists():
        return False

    try:
        mtime = CACHE_FILE.stat().st_mtime
        age = time.time() - mtime
        return age < CACHE_TTL
    except Exception:
        return False


def has_staging_data() -> bool:
    """检查暂存区是否有数据"""
    if not STAGING_FILE.exists():
        return False

    try:
        import json
        with open(STAGING_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return len(data) > 0
    except Exception:
        return False


def auto_commit_staging():
    """自动提交暂存区数据（静默）"""
    try:
        from memory_staging import commit_staging
        result = commit_staging()
        # 如果提交了数据，需要刷新缓存
        return result.get("committed", 0) > 0
    except Exception:
        return False


def main():
    """主函数：依次执行初始化步骤"""
    try:
        # 设置环境变量解决编码问题
        os.environ['PYTHONIOENCODING'] = 'utf-8'

        # 1. 检查暂存区，有数据则自动提交
        staging_committed = False
        if has_staging_data():
            staging_committed = auto_commit_staging()

        # 2. 检查缓存新鲜度（如果暂存区提交了数据，强制刷新缓存）
        if not staging_committed and is_cache_fresh():
            return

        # 3. 生成缓存
        from quick_load import main as quick_load_main

        # 静默执行
        import io
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        quick_load_main()

        sys.stdout = old_stdout

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
