#!/usr/bin/env python3
"""
快速测试脚本 - 只测试关键功能
"""

import sys
import io
from pathlib import Path

# 强制 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def test_visualizations():
    """测试可视化生成"""
    print("=" * 60)
    print("🎨 测试 1: 生成 HTML 可视化")
    print("=" * 60)

    try:
        # 基础版
        print("\n[1/2] 生成基础版 HTML...")
        from memory_visualizer import MemoryVisualizer
        viz = MemoryVisualizer()
        basic_file = viz.generate_html()
        print(f"✓ 基础版已生成: {basic_file}")

        # 增强版
        print("\n[2/2] 生成增强版 HTML (带 ECharts)...")
        from memory_visualizer_enhanced import EnhancedVisualizer
        eviz = EnhancedVisualizer()
        enhanced_file = eviz.generate_enhanced_html()
        print(f"✓ 增强版已生成: {enhanced_file}")

        print("\n" + "─" * 60)
        print("📂 打开以下文件查看效果：")
        print(f"   基础版: file://{basic_file.absolute()}")
        print(f"   增强版: file://{enhanced_file.absolute()}")
        print("─" * 60)

        return basic_file, enhanced_file

    except Exception as e:
        print(f"✗ 可视化测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None, None


def test_reminders():
    """测试智能提醒"""
    print("\n" + "=" * 60)
    print("💝 测试 2: 智能提醒系统")
    print("=" * 60)

    try:
        from smart_reminder import SmartReminder
        reminder = SmartReminder()

        # 获取提醒
        print("\n[1/2] 获取今日提醒...")
        daily_reminders = reminder.get_daily_reminders()

        if daily_reminders:
            print(f"✓ 获取到 {len(daily_reminders)} 条提醒：")
            for i, r in enumerate(daily_reminders, 1):
                print(f"   {i}. {r}")
        else:
            print("  （今天没有特别提醒）")

        # 测试上下文提醒
        print("\n[2/2] 测试上下文提醒...")
        test_contexts = [
            "意外今天怎么样",
            "我在写代码",
        ]

        for ctx in test_contexts:
            ctx_reminder = reminder.get_context_reminder(ctx)
            if ctx_reminder:
                print(f"  用户: '{ctx}' → {ctx_reminder}")

        print("\n✓ 提醒系统测试完成")

    except Exception as e:
        print(f"✗ 提醒测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_encryption():
    """快速测试加密"""
    print("\n" + "=" * 60)
    print("🔐 测试 3: 隐私加密")
    print("=" * 60)

    try:
        from privacy_manager import PrivacyManager
        pm = PrivacyManager()

        # 测试加密解密
        test_text = "这是一个敏感信息：银行卡密码 1234"
        print(f"\n原文: {test_text}")

        encrypted = pm.simple_encrypt(test_text)
        print(f"加密: {encrypted[:50]}...")

        decrypted = pm.simple_decrypt(encrypted)
        print(f"解密: {decrypted}")

        # 验证
        if decrypted == test_text:
            print("✓ 加密解密验证通过")
        else:
            print("✗ 加密解密验证失败")

        # 测试隐私级别检测
        print("\n隐私级别自动检测:")
        test_cases = [
            "今天天气真好",
            "我的密码是123456",
            "个人邮箱 test@example.com"
        ]

        for text in test_cases:
            level = pm.detect_privacy_level(text)
            print(f"  '{text[:20]}...' → {level}")

        print("\n✓ 加密系统测试完成")

    except Exception as e:
        print(f"✗ 加密测试失败: {e}")
        import traceback
        traceback.print_exc()


def show_summary():
    """显示测试总结"""
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)

    outputs_dir = Path(__file__).parent.parent / "user-data" / "outputs"

    print("\n生成的文件位置：")
    print(f"📁 {outputs_dir}")
    print()
    print("目录结构：")
    print("  outputs/")
    print("  ├── html/basic/      ← 基础可视化")
    print("  ├── html/enhanced/   ← 增强可视化 (ECharts)")
    print("  ├── pdf/             ← PDF 报告")
    print("  └── images/posters/  ← 纪念海报")
    print()
    print("=" * 60)
    print()
    print("🎯 下一步测试建议：")
    print()
    print("1. 打开生成的 HTML 查看效果")
    print("2. 使用 PDF skill 转换 HTML → PDF")
    print("3. 使用 canvas-design 生成意外的纪念海报")
    print()
    print("=" * 60)


def main():
    """主测试流程"""
    print("\n" + "🚀 " * 20)
    print("   Claude Memory - 快速测试")
    print("🚀 " * 20 + "\n")

    # 1. 可视化
    basic_html, enhanced_html = test_visualizations()

    # 2. 提醒
    test_reminders()

    # 3. 加密
    test_encryption()

    # 总结
    show_summary()

    print("\n✨ 测试完成！")


if __name__ == "__main__":
    main()