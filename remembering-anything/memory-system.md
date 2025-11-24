# 记忆系统架构详解

## 三层记忆架构

### 1. 结构化记忆 (`user-data/memory/`)

存储经过整理的关键信息，分为三种类型：

#### Facts（事实）
```json
{
  "id": "fact_123",
  "content": "住在杭州",
  "category": "location",
  "source": "chat",
  "timestamp": "2024-11-20T10:00:00",
  "confidence": 0.95,
  "status": "active",
  "importance": "core",
  "context_tags": ["location", "work"],
  "access_count": 5,
  "last_accessed": "2024-11-20T15:00:00"
}
```

**字段说明：**
- `importance`: core（核心）、active（活跃）、contextual（上下文）、archived（归档）
- `status`: active（有效）、deprecated（过时）、conflicted（冲突）
- `supersedes/superseded_by`: 版本控制链接

#### Preferences（偏好）
```json
{
  "id": "pref_456",
  "content": "喜欢简洁的回复风格",
  "category": "communication",
  "importance": "core"
}
```

#### Experiences（经历）
```json
{
  "id": "exp_789",
  "content": "正在开发记忆 skill",
  "category": "work",
  "importance": "active",
  "expires_at": "2024-11-27T10:00:00",
  "is_work_in_progress": true
}
```

### 2. 原始笔记 (`user-data/notes/`)

保留用户的原始输入，作为真实来源：

```
notes/
├── daily/          # 日常记录
│   └── 2024-11-20.md
├── topics/         # 主题笔记
│   ├── python.md
│   └── projects.md
└── projects/       # 项目文档
    └── memory-skill.md
```

### 3. 智能总结 (`user-data/summaries/`)

定期生成的高层次总结：

```
summaries/
├── monthly/        # 月度总结
│   └── 2024-11.md
└── topics/         # 主题总结
    └── coding.md
```

## 分层加载策略

### 重要性层级

| 层级 | 说明 | 加载时机 | 数量限制 | 响应时间 |
|-----|------|---------|---------|----------|
| **Core** | 基础信息（姓名、位置、职业） | 激活时 | 5-10条 | <50ms |
| **Active** | 最近活跃（当前项目、近期话题） | 激活时 | 10-20条 | <100ms |
| **Contextual** | 上下文相关（特定话题） | 按需 | 3-5条 | <100ms |
| **Archived** | 历史归档（旧记忆） | 明确查询 | 不限 | <200ms |

### 加载优化

1. **快速加载脚本** (`quick_load.py`)
   - 预先生成核心记忆缓存
   - 包含最重要的 20-30 条记忆
   - JSON 格式，瞬间读取

2. **缓存机制**
   ```json
   {
     "core_facts": [...],
     "active_experiences": [...],
     "preferences": [...],
     "birthdays": [...],
     "last_updated": "2024-11-20T10:00:00"
   }
   ```

3. **按需查询**
   ```python
   # 只在需要时查询
   if "python" in user_message:
       memories = mm.query_by_context(["python", "coding"])
   ```

## 版本控制机制

### 记忆更新流程

1. **发现新信息**
   ```
   用户："我搬到上海了"
   ```

2. **检测冲突**
   ```python
   # 发现旧记忆："住在杭州"
   conflict = detect_conflict(new="上海", old="杭州")
   ```

3. **创建新版本**
   ```json
   {
     "id": "fact_new",
     "content": "住在上海",
     "status": "active",
     "supersedes": "fact_old"
   }
   ```

4. **标记旧版本**
   ```json
   {
     "id": "fact_old",
     "content": "住在杭州",
     "status": "deprecated",
     "superseded_by": "fact_new"
   }
   ```

## 短期工作记忆

### 自动过期机制

```python
from datetime import datetime, timedelta

# 添加7天后过期的工作状态
expires_at = (datetime.now() + timedelta(days=7)).isoformat()

mm.add_experience(
    content="正在调试性能问题",
    importance="active",
    expires_at=expires_at,
    is_work_in_progress=True
)
```

### 清理策略

每次激活时自动执行：

1. 检查过期记忆
2. 进行中的任务 → 改为已完成
3. 其他过期记忆 → 删除或归档

## 生日提醒系统

### 提醒逻辑

```python
# 1. 提取日期
today = datetime.now().strftime("%m-%d")

# 2. 匹配生日
for fact in facts:
    if fact.get("birthday"):
        if fact["birthday"][5:] == today:
            # 发现生日！

# 3. 分时段提醒
if current_hour < 15:
    slot = "morning"
else:
    slot = "afternoon"

# 4. 避免重复
if not already_reminded(fact_id, slot):
    remind_naturally()
    mark_as_reminded(fact_id, slot)
```

### 提醒日志

```json
{
  "2024-11-20": {
    "morning": ["fact_123"],
    "afternoon": []
  }
}
```

## 笔记搜索集成

### 使用 Claude 原生工具

```python
# 1. 关键词搜索
Grep(pattern="python", path="user-data/notes")

# 2. 读取匹配文件
Read(file_path="user-data/notes/topics/python.md")

# 3. AI 理解和提取
# Claude 自动分析相关性，无需向量数据库
```

### 搜索优化

- 使用文件名模式优先（更快）
- 关键词搜索其次
- 全文搜索最后（较慢）

## 冲突检测

### 自动检测规则

1. **位置变更**：北京 → 杭州
2. **职业变化**：学生 → 开发者
3. **偏好改变**：喜欢 Python → 喜欢 Go

### 处理策略

```python
def handle_conflict(old_memory, new_memory):
    # 1. 标记冲突
    old_memory["status"] = "conflicted"

    # 2. 询问用户
    response = ask_user("你之前说在北京，现在是搬到杭州了吗？")

    # 3. 根据确认更新
    if confirmed:
        new_memory["supersedes"] = old_memory["id"]
        old_memory["status"] = "deprecated"
```

## 性能指标

| 操作 | 目标时间 | 实际时间 |
|------|---------|---------|
| 激活加载 | <1秒 | ~500ms |
| 核心记忆查询 | <100ms | ~50ms |
| 笔记搜索 | <500ms | ~300ms |
| 记忆更新 | <200ms | ~100ms |

## API 使用示例

```python
from memory_manager import MemoryManager

mm = MemoryManager()

# 获取核心记忆
core = mm.get_core_memories()

# 上下文查询
related = mm.query_by_context(["python", "project"])

# 添加新记忆
mm.add_fact(
    content="开始学习 Rust",
    importance="active",
    context_tags=["learning", "rust"]
)

# 检测冲突
conflicts = mm.detect_conflicts()

# 导出备份
mm.export_all("backup.json")
```