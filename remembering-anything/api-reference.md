# API 参考文档

本文档提供 Python 脚本的 API 使用说明。

## MemoryManager 类

主要的记忆管理接口。

### 初始化

```python
from memory_manager import MemoryManager

mm = MemoryManager()
```

### 核心方法

#### 添加记忆

```python
# 添加事实
mm.add_fact(
    content="住在杭州",
    category="location",
    source="chat",
    importance="core",  # core/active/contextual
    context_tags=["location", "work"],
    confidence=0.95
)

# 添加偏好
mm.add_preference(
    content="喜欢简洁的回复",
    category="communication",
    importance="core"
)

# 添加经历
mm.add_experience(
    content="正在开发记忆系统",
    category="work",
    importance="active",
    expires_at="2024-11-27T10:00:00",  # 可选：自动过期
    is_work_in_progress=True  # 标记进行中
)
```

#### 查询记忆

```python
# 获取所有活跃记忆
facts = mm.get_active_facts()
preferences = mm.get_active_preferences()
experiences = mm.get_active_experiences()

# 获取核心记忆（最重要的）
core = mm.get_core_memories()

# 按上下文查询
related = mm.query_by_context(
    tags=["python", "coding"],
    limit=5
)

# 搜索记忆内容
results = mm.search_memories(
    query="项目",
    memory_type="all"  # all/fact/preference/experience
)
```

#### 更新记忆

```python
# 更新记忆内容
mm.update_fact(
    memory_id="fact_123",
    content="现在住在上海",  # 新内容
    supersedes="fact_old"  # 替换旧记忆
)

# 标记记忆状态
mm.update_status(
    memory_id="fact_123",
    status="deprecated"  # active/deprecated/conflicted
)
```

#### 冲突检测

```python
# 检测所有冲突
conflicts = mm.detect_conflicts()

for conflict in conflicts:
    print(f"冲突: {conflict.old_memory} vs {conflict.new_memory}")
    print(f"类型: {conflict.conflict_type}")
    print(f"建议: {conflict.resolution}")
```

#### 版本控制

```python
# 创建新版本（自动处理 supersedes 链）
mm.create_new_version(
    old_id="fact_123",
    new_content="新的内容",
    reason="用户更新"
)

# 获取版本历史
history = mm.get_version_history("fact_123")
```

#### 导入导出

```python
# 导出所有记忆
mm.export_all("backup.json")

# 导出特定类型
mm.export_memories(
    memory_type="fact",
    file_path="facts_backup.json"
)

# 导入记忆
mm.import_memories("backup.json")
```

## 记忆数据结构

### FactMemory

```python
{
    "id": str,                # 唯一标识
    "content": str,           # 记忆内容
    "category": str,          # 分类
    "source": str,            # 来源（chat/note/manual）
    "timestamp": str,         # ISO 格式时间戳
    "confidence": float,      # 置信度 0-1
    "status": str,            # active/deprecated/conflicted
    "importance": str,        # core/active/contextual/archived
    "context_tags": List[str], # 上下文标签
    "access_count": int,      # 访问次数
    "last_accessed": str,     # 最后访问时间
    "supersedes": str,        # 替换的旧记忆ID
    "superseded_by": str,     # 被新记忆替换
    "metadata": dict          # 额外元数据
}
```

### 重要性级别

| 级别 | 说明 | 使用场景 |
|-----|------|---------|
| `core` | 核心记忆 | 基本信息，每次都加载 |
| `active` | 活跃记忆 | 最近常用，优先加载 |
| `contextual` | 上下文记忆 | 特定话题才需要 |
| `archived` | 归档记忆 | 很少使用，按需查询 |

### 状态类型

| 状态 | 说明 |
|-----|------|
| `active` | 当前有效 |
| `deprecated` | 已被新版本替换 |
| `conflicted` | 存在冲突，需要解决 |

## 快速加载脚本

### quick_load.py

生成核心记忆缓存：

```python
python scripts/quick_load.py
```

输出文件：`user-data/memory/.quick_load_cache.json`

### 缓存格式

```json
{
    "user_name": "用户名",
    "core_facts": [...],
    "preferences": [...],
    "active_experiences": [...],
    "birthdays": [
        {
            "name": "意外",
            "date": "06-18",
            "type": "pet",
            "years": 2
        }
    ],
    "stats": {
        "total_memories": 150,
        "notes_count": 23
    },
    "last_updated": "2024-11-20T10:00:00"
}
```

## 命令行工具

### memory_cli.py

```bash
# 查看统计
python scripts/memory_cli.py stats

# 搜索记忆
python scripts/memory_cli.py search "关键词"

# 列出记忆
python scripts/memory_cli.py list --type fact
python scripts/memory_cli.py list --type preference --limit 10

# 检测冲突
python scripts/memory_cli.py conflicts

# 导出备份
python scripts/memory_cli.py export backup.json

# 查看未处理笔记
python scripts/memory_cli.py unprocessed
```

## 笔记搜索

使用 Claude Code 原生工具，无需 Python API：

```python
# 在 Claude Code 中使用
Grep(pattern="关键词", path="user-data/notes")
Read(file_path="user-data/notes/xxx.md")
```

## 路径配置

### path_config.py

自动管理开发/运行环境路径：

```python
from path_config import get_user_data_dir

# 自动返回正确路径
user_data = get_user_data_dir()
# 开发环境: ~/.claude/skills/remembering-anything/user-data/
# 运行环境: ../user-data/
```

## 错误处理

```python
try:
    mm.add_fact(content="测试")
except MemoryError as e:
    print(f"记忆错误: {e}")
except IOError as e:
    print(f"文件错误: {e}")
```

## 性能优化建议

1. **使用快速加载缓存**
   - 启动时只加载缓存
   - 按需查询其他记忆

2. **限制查询数量**
   ```python
   # 好：限制返回数量
   mm.query_by_context(tags, limit=5)

   # 避免：获取所有记忆
   mm.get_all_memories()
   ```

3. **使用重要性分层**
   - 标记 core 记忆（最常用）
   - 定期降级不活跃记忆

4. **批量操作**
   ```python
   # 批量添加
   memories = [...]
   mm.batch_add(memories)
   ```

## 扩展开发

### 自定义记忆类型

```python
class CustomMemory(BaseMemory):
    def __init__(self):
        super().__init__()
        self.custom_field = None

    def validate(self):
        # 自定义验证逻辑
        pass
```

### 插件系统

```python
# 注册自定义处理器
mm.register_processor(
    name="birthday_reminder",
    handler=birthday_handler
)
```