---
name: remembering-anything
description: Use when starting conversations to enable personalized dialogue with long-term memory. Loads user profile, project context, and history. Auto-activates at conversation start for cross-session continuity of preferences, decisions, and dates. (user) - 当需要个性化对话、记住用户背景、了解项目历史或保持跨会话上下文连贯性时使用。
allowed-tools: Bash(python {baseDir}/scripts/*:*), Read, Grep, Write
---

# 记忆系统激活

这个 skill 为 Claude 提供长期记忆能力，通过加载用户画像、项目上下文和历史记忆来实现个性化对话。

---

## 快速参考

| 操作 | 命令 |
|------|------|
| **激活** | `python {baseDir}/scripts/activate.py` |
| **读缓存** | `Read("{baseDir}/user-data/memory/.quick_load_cache.json")` |
| **记新信息** | `python {baseDir}/scripts/memory_staging.py add --type <类型> --content "<内容>"` |
| **搜笔记** | `Grep(pattern="关键词", path="{baseDir}/user-data/notes")` |

**记忆类型**：`fact`(事实) / `preference`(偏好) / `experience`(经历) / `task` / `completed` / `decision` / `pitfall`

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

**触发条件**：用户提到"还记得吗"、"之前说过"、"上次聊的"，或任何暗示需要回忆过去信息的语句。

**查询优先级**：
1. **先查缓存**（激活时已加载）→ `recent`、`user`、`pets`、`project_memory` 等字段
2. **缓存没有** → 读取 `facts.json` / `preferences.json` / `experiences.json`
3. **还没有** → 搜索笔记（见快速参考）
4. **找不到** → 诚实说"这个我不太记得"，**绝不编造**

---

## 持续记忆收集（核心机制）

**这是本 skill 最重要的部分。如果不执行记忆收集，整个系统就是废的。**

---

### 铁律：发现即记录

**用户每说一句话，问自己：这里有没有下次对话有用的信息？**

有 → **立即静默记录**，然后继续回复
没有 → 继续对话

**不记录 = 失忆。没有任何借口可以跳过记录。**

---

### 必须记录的信息（触发器）

用户提到以下任何内容时，**必须立即记录**：

| 触发词 | 类型 | 示例 |
|--------|------|------|
| 位置/城市/出差/搬家 | fact/experience | "我在杭州" → 记 |
| 学习/在学/最近学 | experience | "最近在学 Rust" → 记 |
| 喜欢/习惯/偏好/讨厌 | preference | "我习惯用 Vim" → 记 |
| 决定/选择/用了 | decision | "决定用 PostgreSQL" → 记 |
| 下次/待办/要做/TODO | task | "下次加单元测试" → 记 |
| 完成/搞定/修好了 | completed | "bug 修好了" → 记 |
| 踩坑/问题/注意 | pitfall | "dayjs 时区有坑" → 记 |

---

### 如何记？

```bash
python {baseDir}/scripts/memory_staging.py add --type <类型> --content "<内容>"
```

**类型速查**：
- `fact` - 长期事实（住址、宠物、账号）
- `preference` - 偏好习惯（喜欢/不喜欢）
- `experience` - 近期经历（在学/在做）
- `task` - 项目待办
- `completed` - 项目完成
- `decision` - 项目决策
- `pitfall` - 项目踩坑

---

### 红旗清单 - 发现自己在想这些？停！

- ❌ "这个信息太琐碎了" → **记！琐碎的细节构成完整画像**
- ❌ "修 bug 更紧急" → **记！记录只需 1 秒，不影响任务**
- ❌ "用户会再提的" → **记！大部分信息不会重复第二遍**
- ❌ "不确定分类" → **记！随便选一个类型，总比不记好**
- ❌ "对话快结束了" → **记！现在补记，别让信息流失**
- ❌ "这是临时信息" → **记！临时信息也是 experience**

**看到这些想法出现，就是提醒你：该记录了。**

---

### 合理化借口表

| 借口 | 现实 |
|------|------|
| "这是临时状态，不值得记" | 临时状态就是 experience，记下来 |
| "记太多会污染记忆库" | 不存在的。宁多勿少，系统会去重 |
| "当前任务更重要" | 记录只需 1 秒，和任务并行执行 |
| "下次用户会再说" | 不会的。随口提到的信息只有一次机会 |
| "不确定怎么分类" | 随便选。记错类型比不记好 100 倍 |

---

### 检查点：每次回复前

回复用户之前，花 1 秒检查：

1. 用户这句话里有没有我该记的？
2. 如果有，我记了吗？
3. 没记？**现在记，然后再回复**

**记忆收集和回复并行，不是串行。**

---

**详细分类指南**：参阅 [{baseDir}/references/memory-operations.md](./references/memory-operations.md)

---

## 暂存区自动提交

暂存区的记忆会在**下次激活 skill 时自动提交**到长期记忆。

激活脚本 `activate.py` 会：
1. 检测暂存区是否有数据
2. 有数据则自动提交并整理
3. 然后刷新缓存

**无需手动提交**，下次对话开始时自动处理。

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
