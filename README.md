# Claude Memory

<p align="center">
  <strong>为 Claude 提供长期记忆能力</strong>
</p>

<p align="center">
  一个 Claude Skills 项目，让 AI 记住你的背景、偏好和历史对话
</p>

---

## 🚀 快速开始

### 安装（3 步）

```bash
# 1. 克隆或下载项目
git clone https://github.com/your-username/claude-memory.git

# 2. 复制 remembering-anything 文件夹到 Claude skills 目录
# macOS/Linux:
cp -r claude-memory/remembering-anything ~/.claude/skills/

# Windows:
xcopy /E /I claude-memory\remembering-anything %USERPROFILE%\.claude\skills\remembering-anything

# 3. 在 Claude Code 中唤醒（首次会自动初始化，需等待几秒）
# 直接输入：
夏弥在吗
```

**首次运行**：
- 会自动创建虚拟环境（几秒钟）
- 会自动初始化目录结构
- AI 会以自然方式打招呼

---

## ✨ 核心特性

- 🧠 **三层记忆系统** - 结构化记忆 + 原始笔记 + 智能总结
- 🔄 **记忆版本控制** - 新记忆替换旧记忆，保留历史
- 🎯 **自然对话** - 像朋友一样引用记忆，而不是"根据记录显示..."
- 🌐 **跨项目共享** - 所有项目使用同一份记忆
- ⚡ **零依赖** - 完全使用 Claude Code 原生工具

---

## 📖 使用方法

### 唤醒记忆伙伴

**直接呼唤名字**（推荐）：
```
夏弥
夏弥在吗
夏弥在不在
```

Claude 会自动识别这些呼唤并激活 skill。

### 修改 AI 名字

**⚠️ 已知限制**：改名功能目前**不稳定**，可能无法正常工作。建议使用默认名字"夏弥"。

如需尝试修改，在对话中说：
```
帮我改个名字叫小白
```

**注意**：改名后需要重新启动 Claude Code 才能生效，且可能遇到识别问题。

### 添加笔记

将 Markdown 笔记放入：
```
~/.claude/skills/claude-memory/user-data/notes/
```

然后告诉 AI：
```
我添加了新笔记，请帮我提取记忆
```

---

## 🎭 实现功能

### ✅ 已实现并稳定

1. **笔记搜索**
   - 使用 Claude 原生的 Grep 和 Read 工具
   - 实时搜索，无需构建索引
   - 语义理解，智能匹配

2. **结构化记忆管理**
   - 事实记忆（facts.json）
   - 偏好记忆（preferences.json）
   - 经历记忆（experiences.json）
   - 支持版本控制和冲突检测

3. **用户画像和 AI 画像**
   - 定制 AI 性格和说话风格
   - 记录用户背景和偏好

4. **记忆更新**
   - 新信息自动替换旧信息
   - 保留历史版本
   - 冲突检测和提示

### ⚠️ 已知问题

1. **改名功能不稳定**
   - 修改名字后虽然能激活，但 AI 可能还会记得原来的名字"夏弥"
   - 建议使用默认名字"夏弥"

2. **总结引擎未完全实现**
   - `summary_engine.py` 提供了基础框架
   - 月度总结和主题总结功能需要进一步开发

---

## 📂 项目结构

```
~/.claude/skills/claude-memory/
├── user-data/              # 用户数据（不会被 git 提交）
│   ├── config/             # 用户画像和 AI 画像
│   │   ├── user-persona.md
│   │   └── ai-persona.md
│   ├── memory/             # 结构化记忆
│   │   ├── facts.json
│   │   ├── preferences.json
│   │   └── experiences.json
│   ├── notes/              # 原始笔记
│   └── summaries/          # 智能总结
│
├── remembering-anything/   # Skill 实现
│   ├── SKILL.md            # Skill 配置（包含名字和触发词）
│   ├── assets/             # 模板文件
│   │   ├── ai-persona-template.md
│   │   └── user-persona-template.md
│   └── scripts/            # Python 脚本
│       ├── memory_manager.py      # 记忆管理核心
│       ├── memory_schema.py       # 数据结构
│       ├── memory_cli.py          # 命令行工具
│       ├── note_search.py         # 笔记搜索
│       ├── summary_engine.py      # 总结引擎框架
│       └── setup_directories.py   # 初始化脚本
│
└── .venv/                  # Python 虚拟环境（自动创建）
```

---

## 🔧 命令行工具

```bash
# 进入项目目录
cd ~/.claude/skills/claude-memory

# 查看记忆统计
python remembering-anything/scripts/memory_cli.py stats

# 搜索记忆
python remembering-anything/scripts/memory_cli.py search "关键词"

# 列出所有事实
python remembering-anything/scripts/memory_cli.py list --type fact

# 检测冲突
python remembering-anything/scripts/memory_cli.py conflicts

# 导出备份
python remembering-anything/scripts/memory_cli.py export backup.json
```

---

## 🎯 工作原理

### 笔记搜索

当你说"我之前记录过关于Python的笔记吗？"：

1. AI 使用 `Grep` 工具搜索 `user-data/notes/` 目录
2. 使用 `Read` 工具读取匹配的文件
3. 利用 Claude 的理解能力分析相关性
4. 自然地呈现结果

**优势**：
- ✅ 无需下载大型模型
- ✅ 无需构建向量索引
- ✅ 实时搜索，总是最新
- ✅ Claude 的语义理解比本地模型更强

### 记忆版本控制

```json
// 旧记忆
{
  "id": "mem_001",
  "content": "我住在北京",
  "status": "deprecated",
  "superseded_by": "mem_002"
}

// 新记忆
{
  "id": "mem_002",
  "content": "我住在杭州",
  "status": "active",
  "supersedes": "mem_001"
}
```

AI 会自然地说"知道你现在在杭州"，而不是"根据记录 mem_002..."

---

## ⚠️ 注意事项

### 数据隐私
- 所有数据存储在本地 `user-data/` 目录
- `.gitignore` 已配置排除用户数据
- 不会上传到任何服务器

### 系统要求
- Python 3.8+（用于运行管理脚本）
- Claude Code CLI
- 支持 Windows、macOS、Linux

### 已知限制
1. **改名功能不稳定** - 建议使用默认名字"夏弥"
---

## 🛠️ 故障排查

### 问题：无法激活 skill

**解决方案**：
1. 确认文件夹复制到了正确位置：`~/.claude/skills/remembering-anything/`
2. 检查 `SKILL.md` 文件是否存在
3. 直接呼唤默认名字"夏弥"，不要使用其他名字

### 问题：改名后无法激活

**解决方案**：
1. 恢复默认名字"夏弥"
2. 重新启动 Claude Code
3. 或手动编辑 `remembering-anything/SKILL.md`，将 `name` 改回 `夏弥`

### 问题：首次运行卡住

**解决方案**：
1. 等待至少 30 秒（创建虚拟环境需要时间）
2. 检查网络连接
3. 手动运行初始化：`python remembering-anything/scripts/setup_directories.py`

---

## 📚 更多文档

- **[INSTALL.md](INSTALL.md)** - 详细安装指南
- **[CLAUDE.md](CLAUDE.md)** - 开发文档和架构说明
- **[EXAMPLE.md](EXAMPLE.md)** - 使用示例
- **[CHANGELOG.md](CHANGELOG.md)** - 版本更新历史

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发建议
- 遵循现有代码风格
- 添加必要的注释
- 测试你的更改
- 更新相关文档

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [Claude Code](https://claude.com/claude-code) - Anthropic 官方 CLI 工具

---

<p align="center">
  <sub>让 AI 成为真正了解你的对话伙伴</sub>
</p>
