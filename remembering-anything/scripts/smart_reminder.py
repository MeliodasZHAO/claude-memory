#!/usr/bin/env python3
"""
Smart Reminder System - Generate personalized reminders in 夏弥 style.

This module provides intelligent reminders based on:
- Time-based events (anniversaries, milestones)
- Context-aware suggestions
- Memory patterns and habits
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any


class SmartReminder:
    """Generate smart reminders with personality."""

    def __init__(self):
        """Initialize the reminder system."""
        # Get paths
        self.skill_dir = Path(__file__).parent.parent
        self.user_data = self.skill_dir / "user-data"

        # Load memories
        self.facts = self._load_json("memory/facts.json")
        self.preferences = self._load_json("memory/preferences.json")
        self.experiences = self._load_json("memory/experiences.json")

        # Load or create reminder history
        self.reminder_history = self._load_json("memory/reminder_history.json")

    def _load_json(self, relative_path: str) -> dict:
        """Load JSON file from user-data."""
        file_path = self.user_data / relative_path
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_json(self, data: dict, relative_path: str):
        """Save JSON file to user-data."""
        file_path = self.user_data / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_daily_reminders(self) -> List[str]:
        """Get today's personalized reminders."""
        reminders = []
        now = datetime.now()

        # 1. Special day reminders (意外相关)
        cat_reminder = self._get_cat_reminder()
        if cat_reminder:
            reminders.append(cat_reminder)

        # 2. Project/work reminders
        work_reminders = self._get_work_reminders()
        reminders.extend(work_reminders)

        # 3. Milestone reminders
        milestone_reminders = self._get_milestone_reminders()
        reminders.extend(milestone_reminders)

        # 4. Random memory callback
        if random.random() < 0.3:  # 30% chance
            memory_callback = self._get_memory_callback()
            if memory_callback:
                reminders.append(memory_callback)

        # 5. Time-based reminders (morning/evening)
        time_reminder = self._get_time_based_reminder()
        if time_reminder:
            reminders.append(time_reminder)

        return reminders

    def _get_cat_reminder(self) -> str:
        """Generate cat-related reminder."""
        # Find cat memory
        cat_memory = None
        for mem in self.facts.values():
            if '意外' in mem.get('content', '') or 'cat' in mem.get('tags', []):
                cat_memory = mem
                break

        if not cat_memory:
            return None

        # Calculate days
        timestamp = datetime.fromisoformat(cat_memory['timestamp'].replace('Z', '+00:00'))
        days = (datetime.now() - timestamp).days + 1

        # Different reminders based on milestones
        reminders = []

        if days % 100 == 0:
            reminders.append(f"（探头）哇，今天是和意外一起的第{days}天！整整{days//100}百天了呢")
        elif days % 30 == 0:
            reminders.append(f"（凑近）意外陪你{days//30}个月啦，要不要拍张照纪念一下？")
        elif days % 7 == 0:
            reminders.append(f"（点头）又一周过去了，意外还是那么可爱呢")
        elif random.random() < 0.2:  # 20% chance for random cat reminder
            cat_reminders = [
                "（挠头）意外今天有没有做什么有趣的事？",
                "（探头）记得给意外梳梳毛哦",
                "（眨眼）意外的黄绿色眼睛今天是不是还是那么漂亮？",
                "（凑近）小黑猫今天心情怎么样？"
            ]
            reminders.append(random.choice(cat_reminders))

        return random.choice(reminders) if reminders else None

    def _get_work_reminders(self) -> List[str]:
        """Generate work/project related reminders."""
        reminders = []

        # Check recent experiences for projects
        recent_projects = []
        for exp in self.experiences.values():
            if exp.get('status') == 'active':
                content = exp.get('content', '')
                if '项目' in content or '代码' in content or '开发' in content:
                    # Check last update
                    last_update = datetime.fromisoformat(exp['last_updated'].replace('Z', '+00:00'))
                    days_since = (datetime.now() - last_update).days

                    if days_since > 7:
                        reminders.append(f"（戳戳）那个{content[:20]}...好久没动了，还记得吗？")
                    elif days_since > 3:
                        reminders.append(f"（歪头）{content[:20]}进展怎么样了？")

        return reminders[:2]  # Max 2 work reminders

    def _get_milestone_reminders(self) -> List[str]:
        """Generate milestone reminders."""
        reminders = []
        now = datetime.now()

        # Check for monthly anniversaries
        for fact in self.facts.values():
            if fact.get('category') == 'location':
                timestamp = datetime.fromisoformat(fact['timestamp'].replace('Z', '+00:00'))
                months = (now.year - timestamp.year) * 12 + now.month - timestamp.month

                if months > 0 and now.day == timestamp.day:
                    location = fact.get('content', '某地')
                    reminders.append(f"（回忆）在{location}已经{months}个月了呢")

        return reminders[:1]  # Max 1 milestone reminder

    def _get_memory_callback(self) -> str:
        """Randomly callback an old memory."""
        # Get memories older than 7 days
        old_memories = []
        cutoff = datetime.now() - timedelta(days=7)

        for memory_dict in [self.facts, self.preferences, self.experiences]:
            for mem in memory_dict.values():
                if 'timestamp' in mem:
                    timestamp = datetime.fromisoformat(mem['timestamp'].replace('Z', '+00:00'))
                    if timestamp < cutoff:
                        old_memories.append(mem)

        if not old_memories:
            return None

        memory = random.choice(old_memories)
        content = memory.get('content', '')[:30]

        callbacks = [
            f"（想起什么）还记得之前提到的{content}吗？",
            f"（突然）对了，{content}...后来怎么样了？",
            f"（回忆）前几天说的{content}，现在想想还挺有意思的"
        ]

        return random.choice(callbacks)

    def _get_time_based_reminder(self) -> str:
        """Generate time-appropriate reminders."""
        hour = datetime.now().hour

        morning_reminders = [
            "（伸懒腰）早上好呀，今天准备做点什么？",
            "（揉眼睛）新的一天开始了，有什么计划吗？",
            "（打哈欠）醒了？今天感觉怎么样？"
        ]

        afternoon_reminders = [
            "（探头）下午了，要不要休息一下？",
            "（提醒）别忘了喝水哦",
            "（关心）工作这么久，眼睛累不累？"
        ]

        evening_reminders = [
            "（看时间）晚上了，今天过得怎么样？",
            "（凑近）要不要记录一下今天的事？",
            "（轻声）累了一天，早点休息哦"
        ]

        night_reminders = [
            "（小声）这么晚还不睡吗？",
            "（担心）熬夜对身体不好哦",
            "（打哈欠）困了就去睡吧，明天再继续"
        ]

        if 5 <= hour < 12:
            return random.choice(morning_reminders) if random.random() < 0.3 else None
        elif 12 <= hour < 18:
            return random.choice(afternoon_reminders) if random.random() < 0.2 else None
        elif 18 <= hour < 22:
            return random.choice(evening_reminders) if random.random() < 0.25 else None
        elif hour >= 22 or hour < 5:
            return random.choice(night_reminders) if random.random() < 0.4 else None

        return None

    def get_context_reminder(self, context: str) -> str:
        """Get context-aware reminder based on current conversation."""
        reminders = []

        # Check if context relates to any memories
        for memory_dict in [self.facts, self.preferences, self.experiences]:
            for mem in memory_dict.values():
                content = mem.get('content', '')
                tags = mem.get('tags', []) + mem.get('context_tags', [])

                # Simple keyword matching
                context_lower = context.lower()
                if any(keyword in context_lower for keyword in tags):
                    # Generate relevant reminder
                    if 'python' in tags and 'python' in context_lower:
                        reminders.append("（想起来）上次那个Python性能问题解决了吗？")
                    elif 'work' in tags and ('工作' in context_lower or 'work' in context_lower):
                        reminders.append("（关心）最近工作压力大不大？")
                    elif 'cat' in tags and ('猫' in context_lower or '意外' in context_lower):
                        reminders.append("（笑）意外今天有没有捣蛋？")

        return random.choice(reminders) if reminders else None

    def mark_reminder_shown(self, reminder: str):
        """Mark a reminder as shown to avoid repetition."""
        today = datetime.now().strftime('%Y-%m-%d')
        if today not in self.reminder_history:
            self.reminder_history[today] = []

        self.reminder_history[today].append({
            'reminder': reminder,
            'timestamp': datetime.now().isoformat()
        })

        # Save history
        self._save_json(self.reminder_history, "memory/reminder_history.json")

        # Clean old history (keep only last 30 days)
        cutoff = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        self.reminder_history = {
            date: reminders
            for date, reminders in self.reminder_history.items()
            if date >= cutoff
        }


def main():
    """Test the reminder system."""
    # Force UTF-8 encoding for Windows
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    reminder = SmartReminder()

    # 静默模式：只输出真正的提醒
    daily_reminders = reminder.get_daily_reminders()
    if daily_reminders:
        for r in daily_reminders:
            print(r)
            reminder.mark_reminder_shown(r)
    return  # 静默返回

    # Test context reminders
    test_contexts = [
        "我在写Python代码",
        "今天工作好累",
        "意外又在睡觉"
    ]

    print("情境提醒测试：")
    for context in test_contexts:
        print(f"\n用户: {context}")
        ctx_reminder = reminder.get_context_reminder(context)
        if ctx_reminder:
            print(f"夏弥: {ctx_reminder}")
        else:
            print("夏弥: （专心听你说）")


if __name__ == "__main__":
    main()