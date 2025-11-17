# 使用示例

展示完整的用户体验流程

---

## 场景 1：首次安装和使用

### 用户操作

```bash
# 1. 下载项目
git clone https://github.com/your-repo/claude-memory.git

# 2. 复制到 Claude skills 目录
cp -r claude-memory/remembering-anything ~/.claude/skills/
```

### 在 Claude Code 中

**用户输入**：
```
夏弥在吗
```

**Claude 在后台做的事**（用户看不到）：
1. 检测到没有虚拟环境
2. 自动创建 `.venv`
3. 初始化目录结构
4. 检测到是首次见面

**Claude 的回应**（约 3-5 秒后）：
```
（带着一丝轻松的笑意）好了，线头接上了。

以后你那些散落的念头、没讲完的故事，总算有个地方能帮你妥帖地收好了。

对了，你可以叫我"夏弥"，或者改成你喜欢的名字也行。

想从哪儿开始？
```

---

## 场景 2：修改 AI 名字

**用户在对话中说**：
```
帮我改个名字叫小冰
```

**Claude 的操作**（后台）：
1. 识别用户想改名为"小冰"
2. 修改 SKILL.md 的 name 和 description 字段
3. 自然确认

**Claude 的回应**：
```
（点头）好啊，以后就叫我小冰吧！
```

**之后在 Claude Code 中**：

**用户输入**：
```
小冰在吗
```

**Claude 回应**：
```
（抬头）在的，什么事？
```

---

## 场景 3：日常使用（已配置用户画像）

**用户输入**：
```
夏弥，帮我看看这段代码
```

**Claude 回应**（结合记忆）：
```
（凑近看了眼）这块有点意思啊...

记得你之前在做那个 XX 项目，这个思路和那个类似。想实现什么功能？
```

---

## 场景 4：跨项目记忆持久化

**在项目 A 中**：
```
夏弥，我现在在杭州工作了
```

**Claude**：
```
（点头）好，记下了。

杭州啊，换了新环境感觉怎么样？
```

**在项目 B 中（几天后）**：
```
夏弥在吗
```

**Claude**（自动读取记忆）：
```
嗨，在杭州那边适应得怎么样了？
```

---

## 场景 5：记忆冲突检测

**用户之前说过**：
```
我在北京工作
```

**后来又说**：
```
我现在在杭州了
```

**系统自动检测到冲突**：

旧记忆：
```json
{
  "id": "mem_old123",
  "content": "我在北京工作",
  "status": "deprecated",
  "superseded_by": "mem_new456"
}
```

新记忆：
```json
{
  "id": "mem_new456",
  "content": "我现在在杭州工作",
  "status": "active",
  "supersedes": "mem_old123"
}
```

**Claude 的行为**：
- 不再说"记得你在北京..."
- 改为"知道你现在在杭州..."
- 保留历史记录但不主动提及

---

## 场景 6：查看记忆统计

**用户操作**：
```bash
cd ~/.claude/skills/remembering-anything
python scripts/memory_cli.py stats
```

**输出**：
```
[-] Memory Statistics:
    total_facts: 12
    active_facts: 10
    total_preferences: 8
    active_preferences: 7
    total_experiences: 15
    active_experiences: 15
    fact_categories: 5
    last_updated: 2025-11-17T15:30:22
```

---

## 场景 7：搜索记忆

**用户操作**：
```bash
python scripts/memory_cli.py search "杭州"
```

**输出**：
```
Found 3 memories:

[FACT] 我现在在杭州工作
  Source: chat
  Created: 2025-11-15
  Status: active

[EXPERIENCE] 上周去杭州西湖玩了
  Source: note_2025_11_10.md
  Created: 2025-11-10
  Status: active

[PREFERENCE] 喜欢杭州的天气
  Source: chat
  Created: 2025-11-12
  Status: active
```

---

## 技术细节

### 自动触发机制

**SKILL.md 配置**：
```yaml
---
name: 夏弥
description: 当用户提到"夏弥"、"夏弥在吗"、"夏弥在不在"、或任何呼唤记忆伙伴的表达时激活...
allowed-tools: Read, Grep, Glob, Bash
---
```

**Claude 的匹配逻辑**：
1. 用户输入"夏弥在吗"
2. Claude 扫描所有 skills 的 `name` 和 `description`
3. 发现 `name: 夏弥` 匹配
4. 同时 `description` 包含"夏弥在吗"
5. 双重匹配 → 自动激活此 skill

### 智能判断

**激活**：
- ✅ "夏弥"
- ✅ "夏弥在吗"
- ✅ "夏弥，帮我看看..."

**不激活**（讨论而非呼唤）：
- ❌ "我在看《龙族》，夏弥这个角色..."
- ❌ "你觉得夏弥和绘梨衣谁更强？"

Claude 会根据上下文判断是否是在呼唤 AI。
