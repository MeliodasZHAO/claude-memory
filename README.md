# Claude Memory

<p align="center">
  <strong>让 Claude 拥有关于你的长期记忆</strong>
</p>

<p align="center">
  一个 Claude Skills 项目，通过结构化记忆系统让 AI 真正了解你
</p>

<p align="center">
  <a href="#核心功能">功能</a> •
  <a href="#安装与使用">安装</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#项目结构">结构</a> •
  <a href="#最佳实践">最佳实践</a>
</p>

---

## ✨ 特性一览

🧠 **三层记忆架构** - 结构化记忆 + 原始笔记 + 智能总结
🔄 **自动版本控制** - 新记忆替换旧记忆，保留完整历史
⚡ **增量处理** - 只处理新增内容，高效快速
🎯 **智能引用** - 自然融入记忆，不是机械地"根据记录"
🌐 **全局访问** - 所有项目共享同一份记忆
🔍 **向量检索** - 语义搜索相关笔记和记忆

## 项目简介

Claude Memory 通过整合**用户画像**、**AI 画像**和**向量化个人笔记**，提供个性化的、上下文感知的对话体验。这个技能让 AI 能够记住并引用你之前的想法、偏好和知识库，创造出更加连贯和个性化的交互体验。

**核心优势**：
- ✅ AI 记得你是谁、在哪里、做什么
- ✅ 自动检测并更新过时信息（如搬家、换工作）
- ✅ 自然对话，而非生硬地引用记录
- ✅ 跨项目持久化记忆，一次配置全局使用

## 核心功能

### 🎭 双画像系统
- **用户画像**：定义你的背景、专长、兴趣和沟通偏好
- **AI 画像**：定制 AI 的角色定位、沟通风格和交互方式

### 🧠 三层记忆系统
- **结构化记忆**：自动提取事实、偏好、经历，支持版本控制
- **原始笔记**：保留完整历史，作为真实来源
- **智能总结**：定期生成月度总结和主题总结

### 🔄 记忆更新机制
- **自动冲突检测**：识别矛盾信息（如：北京 → 杭州）
- **版本控制**：新记忆自动替换旧记忆，保留历史
- **来源追踪**：每条记忆都知道它来自哪里
- **增量处理**：只处理新增笔记，不用每次全量重建

### 📝 智能笔记检索
- 自动索引你的 Markdown 笔记
- 根据对话内容智能检索相关历史记录
- 向量检索 + 结构化查询双引擎

### 💬 个性化对话
- 基于结构化记忆和画像生成个性化回应
- 保持对话的上下文连贯性
- 像朋友一样自然地引用你的想法，而非机械地"根据记录"

## 使用场景

当你需要：
- **个性化交流**：AI 知道你是谁，你在哪，你在做什么
- **上下文感知**：AI 能记住你的背景、偏好和经历
- **记忆更新**：位置变了、工作变了，AI 自动更新记忆
- **持续对话**：不管在哪个项目，AI 都记得你
- **智能整理**：把杂乱的笔记整理成结构化的知识

## 安装与使用

### 安装技能

将此项目复制到 `~/.claude/skills/` 文件夹中：

```
~/.claude/skills/
└── claude-memory/           # 本技能包
    ├── user-data/             # ✅ 全局用户数据（所有项目共享）
    │   ├── notes/
    │   ├── config/
    │   └── vector_db/
    ├── .venv/
    ├── assets/
    ├── scripts/
    ├── SKILL.md
    └── README.md
```

### 使用技能

**方式一：通过Skill命令激活**（推荐）
```
/skill claude-memory
```

**方式二：在对话中自然提及**
当你提到个人信息、需要AI记住某些内容时，Claude Code会自动激活此技能。

**首次使用**：
AI会检测到这是首次使用，并友好地询问：
```
👋 欢迎使用 Claude Memory！
你希望现在完善个人信息吗？
1️⃣ 是的，现在设置（推荐）
2️⃣ 稍后设置
```

选择"现在设置"后，AI会引导你创建用户画像和AI画像

### 添加笔记并构建向量数据库

**步骤1：添加你的笔记**
将Markdown笔记放入技能目录下的 `user-data/notes/` 文件夹：
```
user-data/notes/
├── daily/    # 日常笔记
└── topics/   # 主题笔记
```

**步骤2：让AI分析并向量化**
告诉AI：
```
我在 notes 目录放入了笔记，请分析笔记格式，
构建向量数据库，并根据内容推测我的用户画像
```

AI会自动：
1. 分析笔记格式并智能分块
2. 构建向量数据库（使用BAAI/bge-m3模型）
3. 提取事实、偏好、经历到结构化记忆
4. 基于笔记内容生成/更新用户画像

**步骤3：个性化对话**
配置完成后，AI会：
- 自动记住你的背景和偏好
- 在对话中自然引用相关记忆
- 检索历史笔记提供上下文

## 项目结构

### 完整目录结构

**Windows**: `C:\Users\<用户名>\.claude\skills\claude-memory\`
**macOS/Linux**: `~/.claude/skills/claude-memory/`

```
claude-memory/
├── user-data/           # ✅ 全局用户数据（所有项目共享）
│   ├── notes/           # 你的笔记（原始来源）
│   │   ├── daily/       # 日常笔记
│   │   └── topics/      # 主题笔记
│   ├── memory/          # ✅ 结构化记忆
│   │   ├── facts.json          # 事实记忆（我在哪、做什么）
│   │   ├── preferences.json    # 偏好记忆（喜好、习惯）
│   │   ├── experiences.json    # 经历记忆（发生过什么）
│   │   └── metadata.json       # 元数据
│   ├── summaries/       # ✅ 智能总结
│   │   ├── monthly/     # 月度总结
│   │   └── topics/      # 主题总结
│   ├── config/          # 画像配置
│   │   ├── user-persona.md
│   │   └── ai-persona.md
│   └── vector_db/       # 向量数据库
├── .venv/               # Python 虚拟环境
├── scripts/             # 核心脚本
│   ├── memory_schema.py       # ✅ 记忆数据结构
│   ├── memory_manager.py      # ✅ 记忆管理器
│   ├── summary_engine.py      # ✅ 总结引擎
│   ├── memory_cli.py          # ✅ 命令行工具
│   ├── vector_indexer.py
│   └── ...
├── SKILL.md             # 技能详细文档（AI agent 会读取此文件）
└── README.md            # 本文件
```

**核心特性**：
- ✅ **三层记忆架构**：结构化记忆 + 原始笔记 + 智能总结
- ✅ **记忆版本控制**：新记忆可以替换旧记忆，保留历史
- ✅ **冲突检测**：自动发现矛盾信息并提示处理
- ✅ **全局访问**：所有项目共享同一份记忆
- ✅ **增量处理**：只处理新增内容，高效快速

## 工作流程

### 日常对话
1. **加载画像**：读取用户画像和 AI 画像
2. **加载记忆**：获取活跃的事实、偏好、经历
3. **检索上下文**：从向量库检索相关笔记和总结
4. **生成回应**：自然融合记忆，提供个性化回应

### 记忆更新（定期进行）
1. **发现新笔记**：检查未处理的笔记
2. **提取记忆**：从笔记中提取事实、偏好、经历
3. **冲突检测**：与现有记忆对比，发现矛盾
4. **更新记忆**：新记忆替换旧记忆，保留历史
5. **生成总结**：定期整理成月度/主题总结

### 示例：位置变更
```
笔记："我搬到杭州了"
  ↓ AI 提取
旧记忆：{ content: "我住在北京", status: "active" }
新记忆：{ content: "我住在杭州", supersedes: "mem_old" }
  ↓ 自动更新
旧记忆：status → "deprecated"
新记忆：status → "active"
  ↓ 结果
AI 知道你现在在杭州，不再说北京
```

## 特色亮点

### 🧠 智能记忆管理
- **自动更新**：新信息自动替换旧信息（如搬家、换工作）
- **冲突检测**：自动发现矛盾并提示处理
- **来源追踪**：每条记忆都知道它来自哪里
- **版本历史**：旧记忆不删除，标记为 deprecated，可追溯

### 🔄 增量处理
- 不用每次重建整个数据库
- 只处理新增或修改的笔记
- 跟踪处理日志，避免重复工作
- 高效快速，适合日常使用

### 🤖 AI Agent 智能分块
系统会分析每篇笔记的实际格式，动态生成最适合的分块策略，而非使用预设模板。这意味着无论你的笔记是什么格式，都能得到最优处理。

### 🎯 自然引用
AI 会像回忆一样自然地引入你的过往信息，不会生硬地说"根据记录"或"According to memory mem_123"，而是流畅地说"我知道你现在在杭州"。

### 📦 全局数据存储
你的所有数据（笔记、画像、记忆、向量库）都存储在技能目录的 `user-data/` 文件夹中，在任何项目中都能访问。无需迁移，一次配置，全局使用。

## 最佳实践

### 记忆管理
- **定期处理**：每周处理一次新笔记，提取记忆
- **及时更新**：发现信息变化（搬家、换工作）立即更新
- **查看冲突**：定期运行冲突检测，解决矛盾
- **备份导出**：每月导出一次记忆作为备份

### 画像设计
- **具体明确**：模糊的画像会导致通用回复
- **基于记忆更新**：根据累积的记忆更新画像，而非凭空猜测
- **包含示例**：在 AI 画像中展示期望的交互模式

### 笔记管理
- **格式自由**：系统能适应任何笔记结构
- **标注日期**：笔记中包含日期有助于时间追踪
- **主题分类**：用子目录组织（daily/, topics/）
- **内容丰富**：有深度的笔记能带来更好的提取效果

### 提取质量
- **仔细阅读**：理解笔记上下文后再提取
- **保守原则**：不确定的不提取，避免错误记忆
- **检查冲突**：新提取的记忆要对比现有记忆
- **适当标签**：使用标签让记忆易于搜索

## 维护与更新

### 添加新笔记并提取记忆

**让AI自动处理**（推荐）
将新笔记放入 `user-data/notes/` 目录后，告诉AI：
```
我添加了新笔记，请提取记忆并更新向量数据库
```

AI会自动：
1. 检测未处理的笔记
2. 提取事实、偏好、经历
3. 检测与现有记忆的冲突
4. 更新向量数据库

### 命令行工具使用

在技能目录下运行以下命令：

**查看记忆状态**
```bash
# 进入技能目录
cd ~/.claude/skills/claude-memory  # macOS/Linux
cd C:\Users\<用户名>\.claude\skills\claude-memory  # Windows

# 查看统计信息
python scripts/memory_cli.py stats

# 搜索记忆
python scripts/memory_cli.py search "杭州"

# 列出所有事实
python scripts/memory_cli.py list --type fact

# 列出所有偏好
python scripts/memory_cli.py list --type preference

# 检测冲突
python scripts/memory_cli.py conflicts
```

**备份和导出**
```bash
# 导出所有记忆到JSON文件
python scripts/memory_cli.py export backup.json

# 查看未处理的笔记
python scripts/memory_cli.py unprocessed
```

**手动管理记忆**
推荐通过与AI对话来管理记忆，AI会自动调用这些脚本。
如需手动操作，可以使用Python直接调用`memory_manager.py`中的方法

### 更新画像

随着记忆的积累，你可以让AI更新画像：
```
请基于我最近的记忆（facts和preferences）更新我的用户画像
```

AI会分析你的结构化记忆，生成更准确的画像描述

## 注意事项

- **首次运行**：首次构建向量数据库时会自动下载BAAI/bge-m3嵌入模型（约2.5GB），请耐心等待
- **Python环境**：需要Python 3.10+，AI会自动创建虚拟环境并安装依赖
- **数据存储**：所有用户数据存储在技能目录的`user-data/`文件夹
- **全局访问**：无论在哪个项目使用Claude Code，都会访问同一份记忆
- **隐私保护**：`.gitignore`已配置排除`user-data/`，不会被提交到Git
- **记忆管理**：定期检查冲突，及时更新过时的记忆（如搬家、换工作）
- **备份建议**：定期使用`export`命令备份记忆
- **兼容性**：支持Windows、macOS、Linux

## 快速开始

### 第一次使用

**1. 安装技能**
```bash
# 克隆到Claude Skills目录
cd ~/.claude/skills/  # macOS/Linux
cd C:\Users\<用户名>\.claude\skills\  # Windows

git clone <your-repo-url> claude-memory
# 或直接下载并解压到该目录
```

**2. 激活技能**
在Claude Code中输入：
```
/skill claude-memory
```

**3. 首次设置向导**
AI会自动检测并询问：
```
👋 欢迎使用 Claude Memory！
你希望现在完善个人信息吗？
1️⃣ 是的，现在设置（推荐）
2️⃣ 稍后设置
```

**4. 添加笔记并构建索引**
```
# 添加笔记到user-data/notes/目录
# 然后告诉AI：
我添加了笔记，请分析并构建向量数据库
```

**5. 开始个性化对话**
AI会自动记住你的信息，在对话中自然引用相关记忆

### 常用命令

```bash
# 进入技能目录
cd ~/.claude/skills/claude-memory

# 初始化目录结构（首次使用）
python scripts/setup_directories.py

# 查看记忆统计
python scripts/memory_cli.py stats

# 搜索记忆
python scripts/memory_cli.py search "关键词"

# 检测冲突
python scripts/memory_cli.py conflicts

# 导出备份
python scripts/memory_cli.py export backup.json
```

## 更多信息

- **技术文档**：查看`SKILL.md`了解详细的技术实现
- **模板文件**：`assets/`目录包含用户画像和AI画像的模板

## 贡献指南

欢迎贡献！如果你有好的想法或发现了问题：

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发建议

- 遵循现有代码风格
- 添加必要的注释和文档
- 测试你的更改
- 更新相关文档

## 常见问题

**Q: 我的数据安全吗？**
A: 所有数据都存储在本地技能目录的`user-data/`文件夹，完全离线，不会上传到任何服务器。`.gitignore`已配置排除此目录，确保不会被意外提交到Git仓库。

**Q: 向量模型有多大？**
A: 首次运行时会自动下载BAAI/bge-m3嵌入模型（约2.5GB），这是一次性下载，之后会缓存在本地的`~/.cache/huggingface/`目录。

**Q: 可以在多个设备使用吗？**
A: 可以。你可以：
   - 手动同步`user-data/`目录（使用私有云存储或加密工具）
   - 将整个技能目录放在同步文件夹中（如OneDrive、Dropbox）
   - 注意：`.venv/`和`__pycache__/`不需要同步

**Q: 如何备份我的记忆？**
A: 两种方式：
   - **完整备份**：直接备份`user-data/`整个文件夹
   - **导出记忆**：使用`python scripts/memory_cli.py export backup.json`导出结构化记忆

**Q: 支持哪些笔记格式？**
A: 目前支持Markdown格式（.md文件）。AI会智能分析笔记格式并自动生成最优分块策略。

**Q: 如何激活这个技能？**
A: 在Claude Code中输入`/skill claude-memory`，或者在对话中自然提及个人信息时，AI会自动激活此技能。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 致谢

- [Claude Code](https://claude.com/claude-code) - Anthropic 官方 CLI 工具
- [ChromaDB](https://www.trychroma.com/) - 向量数据库
- [BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3) - 多语言嵌入模型

---

<p align="center">
  让 AI 成为真正了解你的对话伙伴，而不仅仅是一个工具
</p>

<p align="center">
  <sub>由社区驱动 • 为个性化对话而生</sub>
</p>
