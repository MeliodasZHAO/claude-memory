#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一激活脚本 - 一步完成所有初始化

功能：
1. 运行 quick_load.py 生成缓存
2. 运行 smart_reminder.py 获取提醒
3. 静默返回，除非有重要提醒
"""

import sys
import os
from pathlib import Path

# 添加脚本目录到路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

def main():
    """主函数：依次执行初始化步骤"""
    try:
        # 设置环境变量解决编码问题
        os.environ['PYTHONIOENCODING'] = 'utf-8'

        # 1. 直接调用 quick_load 的 main 函数
        from quick_load import main as quick_load_main

        # 临时重定向 stdout，静默执行
        import io
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        quick_load_main()

        sys.stdout = old_stdout

        # 2. 检查重要提醒（生日、纪念日等）
        # 暂时跳过 smart_reminder，避免时间提醒和测试输出
        # TODO: 后续优化提醒系统，只显示重要提醒
        pass

        # 静默成功（如果没有提醒，什么都不输出）

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()