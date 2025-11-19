#!/usr/bin/env python3
"""
Memory Visualizer - Generate beautiful HTML visualization of memories.

This script creates an interactive HTML page showing:
- Memory statistics dashboard
- Timeline view
- Special memories (like 意外)
- Tag cloud
- Memory network graph
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter
import random


class MemoryVisualizer:
    """Generate HTML visualization for memories."""

    def __init__(self):
        """Initialize the visualizer."""
        # Get paths
        self.skill_dir = Path(__file__).parent.parent
        self.user_data = self.skill_dir / "user-data"
        self.output_dir = self.user_data / "outputs" / "html" / "basic"

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load memories
        self.facts = self._load_json("memory/facts.json")
        self.preferences = self._load_json("memory/preferences.json")
        self.experiences = self._load_json("memory/experiences.json")

    def _load_json(self, relative_path):
        """Load JSON file from user-data."""
        file_path = self.user_data / relative_path
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def generate_html(self):
        """Generate the main HTML visualization."""
        # Calculate statistics
        stats = self._calculate_stats()

        # Generate timeline data
        timeline = self._generate_timeline()

        # Generate tag cloud
        tag_cloud = self._generate_tag_cloud()

        # Special memory about 意外
        cat_memory = self._get_cat_memory()

        # Create HTML
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>记忆宝库 - Memory Vault</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #fff;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            margin-bottom: 40px;
            animation: fadeIn 1s ease;
        }}

        h1 {{
            font-size: 3em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
        }}

        .stat-card {{
            background: rgba(255,255,255,0.2);
            backdrop-filter: blur(10px);
            padding: 20px 30px;
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.3);
            transition: transform 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
        }}

        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}

        .special-memory {{
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 40px;
            border: 1px solid rgba(255,255,255,0.3);
            animation: slideIn 1s ease;
        }}

        .special-memory h2 {{
            font-size: 1.8em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .cat-info {{
            display: flex;
            gap: 30px;
            align-items: center;
            flex-wrap: wrap;
        }}

        .cat-image {{
            width: 200px;
            height: 200px;
            border-radius: 15px;
            object-fit: cover;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}

        .cat-details {{
            flex: 1;
            min-width: 250px;
        }}

        .cat-details p {{
            margin-bottom: 10px;
            line-height: 1.6;
        }}

        .days-counter {{
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 10px;
            display: inline-block;
            margin-top: 15px;
            font-weight: bold;
        }}

        .timeline-section {{
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 40px;
            border: 1px solid rgba(255,255,255,0.3);
        }}

        .timeline-item {{
            margin-bottom: 20px;
            padding-left: 30px;
            position: relative;
        }}

        .timeline-item::before {{
            content: "•";
            position: absolute;
            left: 10px;
            font-size: 20px;
        }}

        .timeline-date {{
            font-weight: bold;
            margin-bottom: 5px;
            color: #ffd700;
        }}

        .tag-cloud {{
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255,255,255,0.3);
            text-align: center;
        }}

        .tag {{
            display: inline-block;
            padding: 8px 16px;
            margin: 5px;
            background: rgba(255,255,255,0.2);
            border-radius: 20px;
            font-size: 14px;
            transition: all 0.3s ease;
        }}

        .tag:hover {{
            background: rgba(255,255,255,0.3);
            transform: scale(1.1);
        }}

        .tag-large {{ font-size: 20px; font-weight: bold; }}
        .tag-medium {{ font-size: 16px; }}
        .tag-small {{ font-size: 12px; opacity: 0.8; }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>✨ 记忆宝库 ✨</h1>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{stats['total_memories']}</div>
                    <div class="stat-label">条记忆</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['facts_count']}</div>
                    <div class="stat-label">个事实</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['experiences_count']}</div>
                    <div class="stat-label">段经历</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['days_recorded']}</div>
                    <div class="stat-label">天记录</div>
                </div>
            </div>
        </header>

        {cat_memory}

        <section class="timeline-section">
            <h2>📅 记忆时间线</h2>
            <div class="timeline">
                {timeline}
            </div>
        </section>

        <section class="tag-cloud">
            <h2>🏷️ 记忆标签云</h2>
            <div class="tags">
                {tag_cloud}
            </div>
        </section>

        <footer style="text-align: center; margin-top: 50px; opacity: 0.7;">
            <p>Generated with 💜 by Memory Visualizer</p>
            <p>更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </footer>
    </div>
</body>
</html>
"""

        # Save HTML file
        output_file = self.output_dir / f"memory_visualization_{datetime.now().strftime('%Y%m%d')}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"[OK] Visualization generated: {output_file}")
        return output_file

    def _calculate_stats(self):
        """Calculate memory statistics."""
        all_memories = list(self.facts.values()) + list(self.preferences.values()) + list(self.experiences.values())

        # Get date range
        dates = []
        for mem in all_memories:
            if 'timestamp' in mem:
                dates.append(datetime.fromisoformat(mem['timestamp'].replace('Z', '+00:00')))

        days_recorded = 0
        if dates:
            earliest = min(dates)
            days_recorded = (datetime.now() - earliest).days + 1

        return {
            'total_memories': len(all_memories),
            'facts_count': len(self.facts),
            'preferences_count': len(self.preferences),
            'experiences_count': len(self.experiences),
            'days_recorded': days_recorded
        }

    def _generate_timeline(self):
        """Generate timeline HTML."""
        # Collect all memories with timestamps
        timeline_items = []

        for memory_dict in [self.facts, self.preferences, self.experiences]:
            for mem_id, mem in memory_dict.items():
                if 'timestamp' in mem:
                    timeline_items.append({
                        'date': datetime.fromisoformat(mem['timestamp'].replace('Z', '+00:00')),
                        'content': mem.get('content', ''),
                        'type': mem.get('type', 'memory')
                    })

        # Sort by date
        timeline_items.sort(key=lambda x: x['date'], reverse=True)

        # Generate HTML for recent items
        html = ""
        for item in timeline_items[:10]:  # Show last 10 items
            date_str = item['date'].strftime('%Y-%m-%d')
            html += f"""
                <div class="timeline-item">
                    <div class="timeline-date">{date_str}</div>
                    <div class="timeline-content">{item['content']}</div>
                </div>
            """

        return html if html else "<p>暂无时间线数据</p>"

    def _generate_tag_cloud(self):
        """Generate tag cloud HTML."""
        # Collect all tags
        all_tags = []

        for memory_dict in [self.facts, self.preferences, self.experiences]:
            for mem in memory_dict.values():
                if 'tags' in mem:
                    all_tags.extend(mem['tags'])
                if 'context_tags' in mem:
                    all_tags.extend(mem['context_tags'])

        # Count frequency
        tag_counts = Counter(all_tags)

        # Generate HTML
        html = ""
        for tag, count in tag_counts.most_common(20):
            if count >= 3:
                size_class = "tag-large"
            elif count >= 2:
                size_class = "tag-medium"
            else:
                size_class = "tag-small"

            html += f'<span class="tag {size_class}">{tag}</span>'

        return html if html else "<p>暂无标签数据</p>"

    def _get_cat_memory(self):
        """Generate special memory section for 意外."""
        # Find cat-related memory
        cat_memory = None
        for mem in self.facts.values():
            if '意外' in mem.get('content', '') or 'cat' in mem.get('tags', []):
                cat_memory = mem
                break

        if not cat_memory:
            return ""

        # Calculate days with cat
        timestamp = datetime.fromisoformat(cat_memory['timestamp'].replace('Z', '+00:00'))
        days = (datetime.now() - timestamp).days + 1

        # Check if image exists
        image_path = self.user_data / "media" / "images" / "意外.jpg"
        image_html = ""
        if image_path.exists():
            # Use relative path for HTML
            image_html = f'<img src="../../media/images/意外.jpg" alt="意外" class="cat-image">'

        return f"""
        <section class="special-memory">
            <h2>🐱 特别的朋友 - 意外</h2>
            <div class="cat-info">
                {image_html}
                <div class="cat-details">
                    <p><strong>描述：</strong>{cat_memory.get('content', '')}</p>
                    <p><strong>记录时间：</strong>{timestamp.strftime('%Y年%m月%d日')}</p>
                    <div class="days-counter">
                        🎉 今天是和意外一起的第 {days} 天
                    </div>
                </div>
            </div>
        </section>
        """


def main():
    """Main entry point."""
    visualizer = MemoryVisualizer()
    output_file = visualizer.generate_html()
    print(f"\n[i] Open the file in your browser:")
    print(f"    file://{output_file.absolute()}")


if __name__ == "__main__":
    main()