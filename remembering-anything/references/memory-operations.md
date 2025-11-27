# 记忆操作参考

本文档详细说明记忆的分类、暂存区机制和常用操作。

---

## 记忆分类

### 全局记忆（跨项目共享）

#### 1. fact（事实记忆）

**存储位置**：`user-data/memory/facts.json`

**用途**：长期不变的事实信息

**示例**：
- 住在北京
- 养了一只猫叫意外
- GitHub 账号是 xxx
- API 密钥存在 xxx

**判断标准**：如果 1 年后还是事实，就是 fact

---

#### 2. preference（偏好记忆）

**存储位置**：`user-data/memory/preferences.json`

**用途**：个人偏好、习惯、风格

**示例**：
- 喜欢玩英雄联盟
- 喜欢用 TypeScript 而不是 JavaScript
- 偏好简洁的代码风格
- 喜欢看科幻小说

**判断标准**：表达"喜欢/不喜欢"、"偏好"的内容

---

#### 3. experience（经历记忆）

**存储位置**：`user-data/memory/experiences.json`

**用途**：临时的、近期的活动和经历

**特点**：7 天后自动过期

**示例**：
- 最近在学 Python
- 这周在重构项目
- 刚看完《三体》
- 昨天跑了 5 公里

**判断标准**：带有时间性、临时性的事件

---

### 项目记忆（按项目隔离）

**存储位置**：`user-data/memory/projects/<project_id>.json`

- 文件名格式：`owner__repo.json`（`/` 替换为 `__`）
- 非 Git 项目使用目录名作为 project_id
- **无需手动指定项目，自动检测当前所在项目**

#### 1. task（待办任务）

**示例**：
```bash
# 自动检测当前项目，无需 --project 参数
python scripts/memory_staging.py add --type task --content "实现负面反馈机制"
```

#### 2. completed（已完成任务）

**示例**：
```bash
python scripts/memory_staging.py add --type completed --content "提示词优化完成"
```

#### 3. decision（架构决策）

**示例**：
```bash
python scripts/memory_staging.py add --type decision --content "使用 React 而不是 Vue"
```

#### 4. pitfall（踩坑记录）

**示例**：
```bash
python scripts/memory_staging.py add --type pitfall --content "dayjs 时区转换有 bug"
```

---

## 暂存区机制

### 为什么需要暂存区？

对话过程中可能提取到多条记忆，如果每次都立即写入文件：
- 频繁 I/O 操作影响性能
- 无法批量检查和确认
- 难以回滚错误记录

暂存区（`.staging.json`）先临时存储，对话结束时统一提交。

---

### 暂存区操作

#### 添加记忆到暂存区

**全局记忆**：
```bash
python scripts/memory_staging.py add --type fact --content "住在杭州"
python scripts/memory_staging.py add --type preference --content "喜欢喝咖啡"
python scripts/memory_staging.py add --type experience --content "最近在学 Rust"
```

**项目记忆**（自动检测项目，无需指定）：
```bash
python scripts/memory_staging.py add --type task --content "实现用户认证"
python scripts/memory_staging.py add --type decision --content "使用 PostgreSQL"
```

#### 查看暂存区

```bash
python scripts/memory_staging.py list
```

#### 提交到正式记忆

```bash
python scripts/memory_staging.py commit
```

提交后：
- 全局记忆写入 `facts.json` / `preferences.json` / `experiences.json`
- 项目记忆写入 `projects/<项目名>.json`
- 清空暂存区

#### 清空暂存区（不提交）

```bash
python scripts/memory_staging.py clear
```

#### 统计暂存区条目数

```bash
python scripts/memory_staging.py count
```

---

## 常见错误

### ❌ 错误 1：项目信息记成 fact

```bash
# 错误
python scripts/memory_staging.py add --type fact --content "AnyMem 项目待办：实现负面反馈"

# 正确
python scripts/memory_staging.py add --type task --project AnyMem --content "实现负面反馈"
```

### ❌ 错误 2：临时事件记成 fact

```bash
# 错误
python scripts/memory_staging.py add --type fact --content "这周在重构项目"

# 正确
python scripts/memory_staging.py add --type experience --content "这周在重构项目"
```

### ❌ 错误 3：偏好记成 fact

```bash
# 错误
python scripts/memory_staging.py add --type fact --content "喜欢用 Vim"

# 正确
python scripts/memory_staging.py add --type preference --content "喜欢用 Vim"
```

---

## 查询记忆优先级

用户问"我之前说过 XX 吗？"时：

1. **先查缓存**（已加载在内存中）
   - 检查 `.quick_load_cache.json` 的各个字段

2. **再查完整记忆文件**
   ```bash
   Read("user-data/memory/facts.json")
   Read("user-data/memory/preferences.json")
   Read("user-data/memory/experiences.json")
   ```

3. **最后搜索笔记**
   ```bash
   Grep(pattern="关键词", path="user-data/notes", output_mode="files_with_matches")
   ```
   找到匹配文件后用 `Read` 读取内容

4. **找不到就诚实说**
   - "这个我不太记得，能详细说说吗？"
   - 不要编造或猜测

---

## 对话结束时自动提交

当用户表示结束对话（"拜拜"、"下次聊"、"再见"）时，自动执行：

```bash
python scripts/memory_staging.py commit
```

**注意**：静默执行，不要告诉用户"正在提交记忆"。
