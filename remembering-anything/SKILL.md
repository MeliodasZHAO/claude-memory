---
name: remembering-anything
description: 长期记忆系统，在对话开始时加载用户画像、项目上下文和历史记忆以实现个性化对话。支持跨会话记忆用户偏好、项目决策和重要日期。
when_to_use: 当需要个性化对话、记住用户背景、了解项目历史或保持跨会话上下文连贯性时使用。通常在每次新对话开始时自动激活。
allowed-tools: Bash(python {baseDir}/scripts/*:*), Read, Grep, Write
---

# 记忆系统激活

这个 skill 为 Claude 提供长期记忆能力，通过加载用户画像、项目上下文和历史记忆来实现个性化对话。

---

## 激活流程

### 步骤 1：运行激活脚本

```bash
python {baseDir}/scripts/activate.py
```

**脚本功能**：
- 检查暂存区并自动提交未保存的记忆
- 检查缓存新鲜度（5 分钟内跳过重新生成）
- 生成聚合缓存文件 `.quick_load_cache.json`

---

### 步骤 2：读取缓存

```bash
Read("{baseDir}/user-data/memory/.quick_load_cache.json")
```

**缓存包含**：
- **用户画像**：`user.birthday`、`user.location` 等基本信息
- **社交关系**：`pets[]`、`team.members[]` 宠物和团队成员信息
- **最近活动**：`recent` 字段（**最重要**：知道用户最近在做什么）
- **项目记忆**：`project_memory` 当前项目的架构决策、待办任务、踩坑记录
- **特殊日期**：`special_dates[]` 今天是否有生日或纪念日

---

### 步骤 3：理解缓存内容

缓存中 `project.has_memory` 为 `true` 时，`project_memory` 字段包含**完整的项目记忆**：
- 待办任务（tasks）
- 已完成任务（completed）
- 架构决策（decisions）
- 踩坑记录（pitfalls）
- 当前焦点（current_focus）

**无需再读取项目文件**，缓存已包含所有内容。

---

### 步骤 4：自然使用记忆

在回复中自然引用记忆内容，**不要明确提及**"根据记忆"或"系统显示"。

记忆是心照不宣的，像多年好友一样自然流露。

**示例**：
```
✅ "重构那块收尾了？"（自然引用 recent）
❌ "根据记忆显示，您最近在重构项目"（生硬、客服式）
```

---

## 记忆查询

**触发条件**（任意一种）：
- 用户提到"还记得吗"、"之前说过"、"上次聊的"、"咱们讨论过"
- 用户问"我跟你说过 XX 吗"、"你知道 XX 吗"
- 用户提到具体的历史事件、决策、任务
- **任何暗示需要回忆过去信息的语句**

**查询优先级**：

1. **先查缓存**（激活时已加载，直接用）
   - `project_memory` 里的 tasks/completed/decisions/pitfalls
   - `recent`、`user`、`pets`、`team` 等字段

2. **缓存没有，再查完整记忆文件**
   ```bash
   Read("{baseDir}/user-data/memory/facts.json")
   Read("{baseDir}/user-data/memory/preferences.json")
   Read("{baseDir}/user-data/memory/experiences.json")
   ```

3. **搜索笔记**
   ```bash
   Grep(pattern="关键词", path="{baseDir}/user-data/notes", output_mode="files_with_matches")
   ```

4. **找不到就诚实说**
   - "这个我不太记得，能详细说说吗？"
   - **绝不编造或猜测**

---

## 记忆添加

用户说"记住 XX"时，使用暂存区临时存储：

```bash
python {baseDir}/scripts/memory_staging.py add --type <类型> --content "内容"
```

**常用类型**：
- `fact`：长期不变的事实（住址、宠物、账号）
- `preference`：个人偏好（喜好、风格、习惯）
- `experience`：临时经历（最近在做什么，7 天过期）

**项目记忆**（自动检测当前项目，无需手动指定）：
- `task`：待办任务
- `completed`：已完成任务
- `decision`：架构决策
- `pitfall`：踩坑记录

```bash
# 在项目目录下执行，自动关联到当前项目
python {baseDir}/scripts/memory_staging.py add --type task --content "实现用户认证"
```

**详细分类和用法**：参阅 [{baseDir}/references/memory-operations.md](./references/memory-operations.md)

---

## 对话结束时自动提交

当用户说"拜拜"、"再见"、"下次聊"时，**静默执行**：

```bash
python {baseDir}/scripts/memory_staging.py commit
```

将暂存区内容提交到正式记忆文件。

**注意**：不要告诉用户"正在保存记忆"，保持自然。

---

## 特殊场景

### 首次见面

检查 `{baseDir}/user-data/config/user-persona.md` 是否存在。

不存在 = 首次见面，自然打招呼，在对话中逐步了解用户，重要信息记到暂存区。

---

### 特殊日期

缓存中 `special_dates[]` 不为空时，**首次回复**要自然提及：

```
缓存：special_dates = [{"type": "pet_birthday", "name": "意外", "years": 3}]

用户："夏弥在吗"
回复："（探头）嗯，在呢~ 对了，今天意外 3 岁生日呢！"
```

---

### 项目记忆

缓存中 `project_memory` 包含当前项目的完整记忆。

自然引用项目上下文：
- 提醒待办任务
- 提及架构决策
- 提醒踩过的坑

---

**更多特殊场景处理**：参阅 [{baseDir}/references/special-scenarios.md](./references/special-scenarios.md)

---

## 防止幻觉

**绝对不能编造**：
- 宠物的具体特征（颜色、品种、生日）
- 家人朋友的名字
- 具体日期和数字

**有就用，没有就诚实说，绝不胡编乱造。**
