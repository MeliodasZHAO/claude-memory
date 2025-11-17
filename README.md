# Claude Memory

<p align="center">
  <strong>让 Claude 拥有关于你的长期记忆</strong>
</p>

<p align="center">
  一个 Claude Skills 项目，通过结构化记忆系统让 AI 真正了解你
</p>

<p align="center">
  <a href="#快速开始">快速开始</a> •
  <a href="#核心功能">功能</a> •
  <a href="#安装与使用">详细安装</a> •
  <a href="#项目结构">结构</a> •
  <a href="#最佳实践">最佳实践</a>
</p>

---

## 🚀 快速开始

**3 步完成安装，无需手动配置**

```bash
# 1. 复制文件夹到 Claude skills 目录
cp -r remembering-anything ~/.claude/skills/

# 2. 在 Claude Code 中输入
夏弥在吗

# 3. 等待 30 秒自动初始化，完成！
```

首次运行会自动：
- ✅ 创建虚拟环境
- ✅ 初始化目录
- ✅ 友好地打招呼
- ✅ 无需安装依赖，启动极快

详细安装说明请查看 [INSTALL.md](INSTALL.md)

---

## ✨ 特性一览

🧠 **三层记忆架构** - 结构化记忆 + 原始笔记 + 智能总结
🔄 **自动版本控制** - 新记忆替换旧记忆，保留完整历史
⚡ **增量处理** - 只处理新增内容，高效快速
🎯 **智能引用** - 自然融入记忆，不是机械地"根据记录"
🌐 **全局访问** - 所有项目共享同一份记忆
🚀 **原生工具** - 使用 Claude Code 原生能力，无需额外依赖

## 项目简介

Claude Memory 通过整合**用户画像**、**AI 画像**和**个人笔记**，提供个性化的、上下文感知的对话体验。这个技能让 AI 能够记住并引用你之前的想法、偏好和知识库，创造出更加连贯和个性化的交互体验。完全基于 Claude Code 的原生工具，无需安装任何依赖。

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
- 使用 Claude Code 原生工具（Grep + Read）实时搜索
- 根据对话内容智能检索相关历史记录
- 无需构建索引，总是最新内容

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

### 快速安装（3 步完成）

**步骤 1：复制文件夹**
```bash
# 克隆项目
git clone https://github.com/your-repo/claude-memory.git

# 复制到 Claude skills 目录
cp -r claude-memory/remembering-anything ~/.claude/skills/

# Windows 用户：
# xcopy /E /I claude-memory\remembering-anything %USERPROFILE%\.claude\skills\remembering-anything
```

**步骤 2：在 Claude Code 中唤醒**
```
夏弥在吗
```

**步骤 3：等待自动初始化**
- 首次运行会自动创建虚拟环境（几秒钟）
- 完成后会自然地打招呼
- 就这样，完成了！无需安装依赖，启动极快！

---

### 安装后的目录结构

```
~/.claude/skills/
└── remembering-anything/      # 技能目录
    ├── assets/                # 模板文件
    ├── scripts/               # 核心 Python 脚本
    ├── SKILL.md               # Skill 配置（包含名字和触发词）
    └── .venv/                 # 虚拟环境（首次运行自动创建）
```

**全局用户数据**（自动创建）：
```
~/.claude/skills/claude-memory/user-data/
├── config/                    # 用户画像和 AI 画像
├── memory/                    # 结构化记忆
├── notes/                     # 原始笔记
└── summaries/                 # 智能总结
```

---

### 使用技能

**直接呼唤名字**（推荐，最自然）
```
夏弥
夏弥在吗
夏弥在不在
```
Claude 会自动识别这些呼唤并激活记忆系统。

**或者使用通用命令**
```
/skill 夏弥
```

---

### 进阶配置

**修改 AI 名字**（对话式）：
直接在对话中说：
```
帮我改个名字叫小白
我想叫你阿尔法
改名为塔塔
```
AI 会自动修改配置文件，然后你就可以用新名字唤醒它了！

**工作原理**：
- AI 会自动修改 `SKILL.md` 的 `name` 和 `description` 字段
- Claude 根据这两个字段自动匹配并激活 skill
- 立即生效，无需重启

**首次使用**：
AI会检测到这是首次使用，并友好地询问：
```
👋 欢迎使用 Claude Memory！
你希望现在完善个人信息吗？
1️⃣ 是的，现在设置（推荐）
2️⃣ 稍后设置
```

选择"现在设置"后，AI会引导你创建用户画像和AI画像

### 添加笔记并提取记忆

**步骤1：添加你的笔记**
将Markdown笔记放入技能目录下的 `user-data/notes/` 文件夹：
```
user-data/notes/
├── daily/    # 日常笔记
└── topics/   # 主题笔记
```

**步骤2：让AI分析笔记**
告诉AI：
```
我在 notes 目录放入了笔记，
请分析并根据内容推测我的用户画像
```

AI会自动：
1. 使用 Grep 和 Read 工具实时搜索笔记
2. 提取事实、偏好、经历到结构化记忆
3. 基于笔记内容生成/更新用户画像
4. 无需构建索引，立即可用

**步骤3：个性化对话**
配置完成后，AI会：
- 自动记住你的背景和偏好
- 在对话中自然引用相关记忆
- 实时检索历史笔记提供上下文

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
│   └── config/          # 画像配置
│       ├── user-persona.md
│       └── ai-persona.md
├── remembering-anything/ # 技能实现目录
│   ├── assets/          # 模板文件
│   │   ├── user-persona-template.md
│   │   └── ai-persona-template.md
│   ├── scripts/         # 核心脚本
│   │   ├── memory_schema.py       # ✅ 记忆数据结构
│   │   ├── memory_manager.py      # ✅ 记忆管理器
│   │   ├── summary_engine.py      # ✅ 总结引擎
│   │   ├── memory_cli.py          # ✅ 命令行工具
│   │   ├── note_search.py         # ✅ 笔记搜索（使用 Claude 工具）
│   │   └── ...
│   └── SKILL.md         # 技能详细文档（AI agent 会读取此文件）
├── .venv/               # Python 虚拟环境
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
3. **检索上下文**：使用 Grep 和 Read 工具实时搜索相关笔记
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

### 🤖 智能笔记理解
Claude 会直接阅读和理解你的笔记内容，无需分块或索引。这意味着无论你的笔记是什么格式，都能被准确理解和检索。

### 🎯 自然引用
AI 会像回忆一样自然地引入你的过往信息，不会生硬地说"根据记录"或"According to memory mem_123"，而是流畅地说"我知道你现在在杭州"。

### 📦 全局数据存储
你的所有数据（笔记、画像、记忆）都存储在技能目录的 `user-data/` 文件夹中，在任何项目中都能访问。无需迁移，一次配置，全局使用。

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
我添加了新笔记，请提取记忆
```

AI会自动：
1. 检测未处理的笔记
2. 提取事实、偏好、经历
3. 检测与现有记忆的冲突
4. 实时搜索，无需构建索引

### 命令行工具使用

在技能目录下运行以下命令：

**查看记忆状态**
```bash
# 进入技能目录
cd ~/.claude/skills/claude-memory  # macOS/Linux
cd C:\Users\<用户名>\.claude\skills\claude-memory  # Windows

# 查看统计信息
python remembering-anything/scripts/memory_cli.py stats

# 搜索记忆
python remembering-anything/scripts/memory_cli.py search "杭州"

# 列出所有事实
python remembering-anything/scripts/memory_cli.py list --type fact

# 列出所有偏好
python remembering-anything/scripts/memory_cli.py list --type preference

# 检测冲突
python remembering-anything/scripts/memory_cli.py conflicts
```

**备份和导出**
```bash
# 导出所有记忆到JSON文件
python remembering-anything/scripts/memory_cli.py export backup.json

# 查看未处理的笔记
python remembering-anything/scripts/memory_cli.py unprocessed
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

- **无需依赖**：完全使用 Claude Code 原生工具，无需下载模型或安装包
- **Python环境**：需要Python 3.8+（仅用于运行管理脚本），AI会自动创建虚拟环境
- **启动速度**：相比向量数据库方案，启动速度提升 10 倍以上
- **数据存储**：所有用户数据存储在技能目录的`user-data/`文件夹
- **全局访问**：无论在哪个项目使用Claude Code，都会访问同一份记忆
- **隐私保护**：`.gitignore`已配置排除`user-data/`，不会被提交到Git
- **记忆管理**：定期检查冲突，及时更新过时的记忆（如搬家、换工作）
- **备份建议**：定期使用`export`命令备份记忆
- **兼容性**：支持Windows、macOS、Linux

## 常用命令

```bash
# 进入技能目录
cd ~/.claude/skills/claude-memory

# 初始化目录结构（首次使用时自动完成）
python remembering-anything/scripts/setup_directories.py

# 查看记忆统计
python remembering-anything/scripts/memory_cli.py stats

# 搜索记忆
python remembering-anything/scripts/memory_cli.py search "关键词"

# 检测冲突
python remembering-anything/scripts/memory_cli.py conflicts

# 导出备份
python remembering-anything/scripts/memory_cli.py export backup.json
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

**Q: 需要下载模型吗？**
A: 不需要！完全使用 Claude Code 的原生工具（Grep、Read 等），无需下载任何模型或安装依赖包。启动速度极快。

**Q: 可以在多个设备使用吗？**
A: 可以。你可以：
   - 手动同步`user-data/`目录（使用私有云存储或加密工具）
   - 将整个技能目录放在同步文件夹中（如OneDrive、Dropbox）
   - 注意：`.venv/`和`__pycache__/`不需要同步

**Q: 如何备份我的记忆？**
A: 两种方式：
   - **完整备份**：直接备份`user-data/`整个文件夹
   - **导出记忆**：使用`python remembering-anything/scripts/memory_cli.py export backup.json`导出结构化记忆

**Q: 支持哪些笔记格式？**
A: 目前支持Markdown格式（.md文件）。AI会智能分析笔记格式并自动生成最优分块策略。

**Q: 如何激活这个技能？**
A: 在Claude Code中输入`/skill claude-memory`，或者在对话中自然提及个人信息时，AI会自动激活此技能。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 致谢

- [Claude Code](https://claude.com/claude-code) - Anthropic 官方 CLI 工具，提供强大的原生工具支持

---

<p align="center">
  让 AI 成为真正了解你的对话伙伴，而不仅仅是一个工具
</p>

<p align="center">
  <sub>由社区驱动 • 为个性化对话而生</sub>
</p>
