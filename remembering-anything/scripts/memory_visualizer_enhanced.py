#!/usr/bin/env python3
"""
Enhanced Memory Visualizer - Generate interactive HTML with ECharts.

Features:
- Memory network graph (relationships between memories)
- Growth trend charts
- Interactive timeline
- Advanced tag cloud
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import random


class EnhancedVisualizer:
    """Generate enhanced HTML visualization with charts."""

    def __init__(self):
        """Initialize the visualizer."""
        self.skill_dir = Path(__file__).parent.parent
        self.user_data = self.skill_dir / "user-data"
        self.output_dir = self.user_data / "visualizations"
        self.output_dir.mkdir(exist_ok=True)

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

    def generate_enhanced_html(self):
        """Generate enhanced HTML with ECharts."""
        # Generate all data
        stats = self._calculate_stats()
        cat_memory = self._get_cat_memory()
        timeline = self._generate_timeline()
        tag_cloud = self._generate_tag_cloud()
        network_data = self._generate_network_data()
        growth_data = self._generate_growth_data()

        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>记忆宝库 - Enhanced Visualization</title>
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
            max-width: 1400px;
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
            gap: 30px;
            flex-wrap: wrap;
            margin-bottom: 30px;
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

        .section {{
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            border: 1px solid rgba(255,255,255,0.3);
            animation: slideIn 1s ease;
        }}

        h2 {{
            font-size: 1.8em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .chart-container {{
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
        }}

        .grid-layout {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 30px;
        }}

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
            <h1>✨ 记忆宝库 - 增强版 ✨</h1>
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

        <div class="grid-layout">
            <section class="section">
                <h2>🕸️ 记忆关系网络</h2>
                <div class="chart-container">
                    <div id="network-chart" style="width: 100%; height: 400px;"></div>
                </div>
            </section>

            <section class="section">
                <h2>📊 记忆增长趋势</h2>
                <div class="chart-container">
                    <div id="growth-chart" style="width: 100%; height: 400px;"></div>
                </div>
            </section>
        </div>

        <section class="section">
            <h2>🗓️ 记忆热力图</h2>
            <div class="chart-container">
                <div id="heatmap-chart" style="width: 100%; height: 300px;"></div>
            </div>
        </section>

        <section class="section">
            <h2>📈 标签分布</h2>
            <div class="chart-container">
                <div id="tags-chart" style="width: 100%; height: 350px;"></div>
            </div>
        </section>

        <footer style="text-align: center; margin-top: 50px; opacity: 0.7;">
            <p>Generated with 💜 by Enhanced Memory Visualizer</p>
            <p>更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </footer>
    </div>

    <!-- ECharts -->
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <script>
        // 配置主题色
        var themeColors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe'];

        // 1. 记忆关系网络图
        var networkChart = echarts.init(document.getElementById('network-chart'));
        var networkOption = {network_data};
        networkChart.setOption(networkOption);

        // 2. 记忆增长趋势图
        var growthChart = echarts.init(document.getElementById('growth-chart'));
        var growthOption = {growth_data};
        growthChart.setOption(growthOption);

        // 3. 记忆热力图
        var heatmapChart = echarts.init(document.getElementById('heatmap-chart'));
        var heatmapOption = {self._generate_heatmap_data()};
        heatmapChart.setOption(heatmapOption);

        // 4. 标签分布图
        var tagsChart = echarts.init(document.getElementById('tags-chart'));
        var tagsOption = {self._generate_tags_chart_data()};
        tagsChart.setOption(tagsOption);

        // 响应式调整
        window.addEventListener('resize', function() {{
            networkChart.resize();
            growthChart.resize();
            heatmapChart.resize();
            tagsChart.resize();
        }});
    </script>
</body>
</html>
"""
        # Save HTML file
        output_file = self.output_dir / f"enhanced_visualization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"[OK] Enhanced visualization generated: {output_file}")
        return output_file

    def _calculate_stats(self):
        """Calculate memory statistics."""
        all_memories = list(self.facts.values()) + list(self.preferences.values()) + list(self.experiences.values())

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

    def _get_cat_memory(self):
        """Generate special memory section for 意外."""
        cat_memory = None
        for mem in self.facts.values():
            if '意外' in mem.get('content', '') or 'cat' in mem.get('tags', []):
                cat_memory = mem
                break

        if not cat_memory:
            return ""

        timestamp = datetime.fromisoformat(cat_memory['timestamp'].replace('Z', '+00:00'))
        days = (datetime.now() - timestamp).days + 1

        return f"""
        <section class="section" style="background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,200,100,0.2));">
            <h2>🐱 特别的朋友 - 意外</h2>
            <p style="font-size: 1.1em; line-height: 1.6;">
                {cat_memory.get('content', '')}
            </p>
            <div style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.2); border-radius: 10px; display: inline-block;">
                🎉 今天是和意外一起的第 <span style="font-size: 1.5em; font-weight: bold;">{days}</span> 天
            </div>
        </section>
        """

    def _generate_timeline(self):
        """Generate timeline HTML."""
        timeline_items = []
        for memory_dict in [self.facts, self.preferences, self.experiences]:
            for mem in memory_dict.values():
                if 'timestamp' in mem:
                    timeline_items.append({
                        'date': datetime.fromisoformat(mem['timestamp'].replace('Z', '+00:00')),
                        'content': mem.get('content', ''),
                        'type': mem.get('type', 'memory')
                    })

        timeline_items.sort(key=lambda x: x['date'], reverse=True)
        return timeline_items[:10]

    def _generate_tag_cloud(self):
        """Generate tag cloud data."""
        all_tags = []
        for memory_dict in [self.facts, self.preferences, self.experiences]:
            for mem in memory_dict.values():
                if 'tags' in mem:
                    all_tags.extend(mem['tags'])
                if 'context_tags' in mem:
                    all_tags.extend(mem['context_tags'])
        return Counter(all_tags)

    def _generate_network_data(self):
        """Generate network graph data for ECharts."""
        nodes = []
        links = []

        # Create nodes for each memory type
        nodes.append({'id': 'center', 'name': '记忆核心', 'symbolSize': 50, 'category': 0})
        nodes.append({'id': 'facts', 'name': '事实', 'symbolSize': 40, 'category': 1})
        nodes.append({'id': 'prefs', 'name': '偏好', 'symbolSize': 40, 'category': 2})
        nodes.append({'id': 'exps', 'name': '经历', 'symbolSize': 40, 'category': 3})

        # Connect to center
        links.append({'source': 'center', 'target': 'facts'})
        links.append({'source': 'center', 'target': 'prefs'})
        links.append({'source': 'center', 'target': 'exps'})

        # Add important memories as nodes
        tag_connections = defaultdict(list)

        for mem in list(self.facts.values())[:5]:
            node_id = f"fact_{mem.get('id', '')[:8]}"
            nodes.append({
                'id': node_id,
                'name': mem.get('content', '')[:20],
                'symbolSize': 20,
                'category': 1
            })
            links.append({'source': 'facts', 'target': node_id})

            # Track tags for connections
            for tag in mem.get('tags', []):
                tag_connections[tag].append(node_id)

        # Create connections between memories with same tags
        for tag, node_ids in tag_connections.items():
            if len(node_ids) > 1:
                for i in range(len(node_ids) - 1):
                    links.append({
                        'source': node_ids[i],
                        'target': node_ids[i + 1],
                        'lineStyle': {'type': 'dashed', 'opacity': 0.5}
                    })

        return json.dumps({
            'tooltip': {'trigger': 'item'},
            'legend': {
                'data': ['核心', '事实', '偏好', '经历'],
                'textStyle': {'color': '#fff'}
            },
            'series': [{
                'type': 'graph',
                'layout': 'force',
                'data': nodes,
                'links': links,
                'categories': [
                    {'name': '核心'},
                    {'name': '事实'},
                    {'name': '偏好'},
                    {'name': '经历'}
                ],
                'roam': True,
                'label': {'show': True, 'color': '#fff'},
                'lineStyle': {'color': 'source', 'curveness': 0.3},
                'force': {
                    'repulsion': 1000,
                    'gravity': 0.1,
                    'edgeLength': 100
                }
            }]
        }, ensure_ascii=False)

    def _generate_growth_data(self):
        """Generate growth trend data for ECharts."""
        # Collect dates
        date_counts = defaultdict(int)

        for memory_dict in [self.facts, self.preferences, self.experiences]:
            for mem in memory_dict.values():
                if 'timestamp' in mem:
                    date = datetime.fromisoformat(mem['timestamp'].replace('Z', '+00:00')).date()
                    date_counts[date] += 1

        if not date_counts:
            return json.dumps({'title': {'text': '暂无数据'}})

        # Generate cumulative data
        sorted_dates = sorted(date_counts.keys())
        dates = []
        values = []
        cumulative = 0

        for date in sorted_dates:
            dates.append(date.strftime('%Y-%m-%d'))
            cumulative += date_counts[date]
            values.append(cumulative)

        return json.dumps({
            'title': {
                'text': '记忆累积增长',
                'textStyle': {'color': '#fff'}
            },
            'tooltip': {
                'trigger': 'axis',
                'axisPointer': {'type': 'shadow'}
            },
            'xAxis': {
                'type': 'category',
                'data': dates,
                'axisLabel': {'color': '#fff'}
            },
            'yAxis': {
                'type': 'value',
                'axisLabel': {'color': '#fff'}
            },
            'series': [{
                'name': '累积记忆数',
                'type': 'line',
                'smooth': True,
                'areaStyle': {
                    'color': {
                        'type': 'linear',
                        'x': 0, 'y': 0, 'x2': 0, 'y2': 1,
                        'colorStops': [
                            {'offset': 0, 'color': 'rgba(102, 126, 234, 0.8)'},
                            {'offset': 1, 'color': 'rgba(118, 75, 162, 0.2)'}
                        ]
                    }
                },
                'data': values
            }]
        }, ensure_ascii=False)

    def _generate_heatmap_data(self):
        """Generate heatmap data for memory activity."""
        # This would need actual date-based activity data
        # For now, returning a placeholder
        return json.dumps({
            'title': {
                'text': '记忆活动热力图',
                'textStyle': {'color': '#fff'}
            },
            'tooltip': {'position': 'top'},
            'visualMap': {
                'min': 0,
                'max': 10,
                'calculable': True,
                'orient': 'horizontal',
                'left': 'center',
                'bottom': '15%',
                'textStyle': {'color': '#fff'}
            },
            'series': [{
                'type': 'heatmap',
                'data': [],
                'label': {'show': True}
            }]
        }, ensure_ascii=False)

    def _generate_tags_chart_data(self):
        """Generate tags distribution chart."""
        tag_counts = self._generate_tag_cloud()

        if not tag_counts:
            return json.dumps({'title': {'text': '暂无标签数据'}})

        # Get top 10 tags
        top_tags = tag_counts.most_common(10)
        tags = [tag for tag, _ in top_tags]
        counts = [count for _, count in top_tags]

        return json.dumps({
            'title': {
                'text': '热门标签分布',
                'textStyle': {'color': '#fff'}
            },
            'tooltip': {
                'trigger': 'item',
                'formatter': '{b}: {c} ({d}%)'
            },
            'series': [{
                'type': 'pie',
                'radius': ['40%', '70%'],
                'avoidLabelOverlap': False,
                'itemStyle': {
                    'borderRadius': 10,
                    'borderColor': '#fff',
                    'borderWidth': 2
                },
                'label': {
                    'show': True,
                    'color': '#fff'
                },
                'data': [{'name': tag, 'value': count} for tag, count in top_tags]
            }]
        }, ensure_ascii=False)


def main():
    """Generate enhanced visualization."""
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    visualizer = EnhancedVisualizer()
    output_file = visualizer.generate_enhanced_html()
    print(f"\n[i] Open in browser: file://{output_file.absolute()}")


if __name__ == "__main__":
    main()