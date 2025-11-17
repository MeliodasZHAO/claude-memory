# 更新日志

## [3.0.0] - 2025-11-17

### 🚀 重大升级：拥抱 Claude Code 原生能力

**核心理念**：既然是 Claude Code 的 skill，就应该充分利用 Claude 的能力，而非依赖外部工具。

### ✨ 重大变化

#### 1. 移除向量数据库依赖
- **移除**：ChromaDB + sentence-transformers
- **移除**：BAAI/bge-m3 模型（~2.5GB）
- **替代方案**：使用 Claude Code 原生的 Grep 和 Read 工具
- **优势**：
  - ✅ 无需下载大型模型
  - ✅ 无需构建索引
  - ✅ 启动速度提升 10 倍以上
  - ✅ 实时搜索，总是最新内容
  - ✅ Claude 的语义理解能力比本地模型更强

#### 2. 对话式改名功能
- **新增**：直接在对话中说"帮我改个名字叫XX"即可修改 AI 名字
- **原理**：SKILL.md 中添加了改名功能说明，agent 自动调用 `name_manager.py`
- **优势**：无需手动输入命令，更符合 Claude Code 的使用方式

### 🗑️ 移除的文件和依赖

**已归档**（重命名为 .deprecated）：
- `vector_indexer.py` → `vector_indexer.py.deprecated`
- `vector_query.py` → `vector_query.py.deprecated`
- `build_vector_db.py` → `build_vector_db.py.deprecated`

**依赖清空**：
- `requirements.txt` 现在不包含任何依赖
- 完全使用 Claude Code 原生工具

### 📝 新增功能

#### 笔记搜索（基于 Claude 原生工具）

**工作流程**：
1. 使用 `Grep` 工具在 `user-data/notes/` 目录中搜索关键词
2. 使用 `Read` 工具读取匹配的文件
3. 利用 Claude 的理解能力判断相关性，提取关键信息
4. 自然呈现结果（不说"查询到3条记录"）

**示例**：
```
用户："我之前记录过关于Python的笔记吗？"
Agent：
1. Grep(pattern="Python", path="user-data/notes")
2. Read() 读取匹配文件
3. 分析并自然回应："哟，找到了！你之前记过XX和XX，要不要看看？"
```

#### 对话式改名

**触发方式**：
- "帮我改个名字叫小白"
- "我想叫你阿尔法"
- "改名为塔塔"

**处理流程**：
1. 识别用户想修改 AI 名字
2. 提取新名字
3. 调用 `name_manager.py set <新名字>`
4. 自然确认："（点头）好啊，以后就叫我小白吧！"

### 📚 文档更新

#### 更新的文档
- **README.md**：
  - 移除所有向量数据库相关描述
  - 更新特性列表
  - 添加对话式改名说明
  - 更新安装说明（无需依赖）

- **CLAUDE.md**：
  - 移除 ChromaDB 和模型相关说明
  - 添加笔记搜索的新方法
  - 更新注意事项
  - 强调启动速度提升

- **SKILL.md**：
  - 添加详细的笔记搜索工作流程
  - 添加对话式改名功能说明
  - 移除向量数据库构建说明

- **INSTALL.md**：
  - 更新安装时间说明（从 30-60 秒 → 几秒钟）
  - 移除依赖安装相关问题
  - 添加对话式改名示例

#### 新增文件
- **note_search.py**：提供基于 Claude 工具的笔记搜索思路和辅助函数

### 🎯 性能对比

#### 安装速度
- **之前**：首次运行 30-60 秒（下载模型 + 安装依赖）
- **现在**：首次运行 3-5 秒（只创建虚拟环境）
- **提升**：10 倍以上

#### 磁盘占用
- **之前**：~3GB（模型 2.5GB + 依赖包 0.5GB）
- **现在**：~10MB（只有 Python 脚本）
- **减少**：99.7%

#### 笔记搜索
- **之前**：需要预先构建索引（几分钟）
- **现在**：实时搜索，无需构建
- **优势**：总是最新内容，无需维护索引

### ⚠️ 破坏性变更

#### 对现有用户
如果你之前使用过 2.x 版本：

1. **更新代码**：
   ```bash
   cd ~/.claude/skills/claude-memory
   git pull  # 或重新下载
   ```

2. **无需操作**：
   - 旧的向量数据库文件会被忽略
   - 结构化记忆（facts/preferences/experiences）完全兼容
   - 笔记文件无需任何修改

3. **清理旧数据**（可选）：
   ```bash
   rm -rf user-data/vector_db  # 删除旧的向量数据库
   rm -rf ~/.cache/huggingface  # 删除缓存的模型
   ```

### 🐛 Bug 修复

- 移除了向量数据库相关的潜在错误
- 简化了依赖管理

### 📊 用户体验提升

- **安装体验**：从"等待下载模型"到"几秒完成"
- **使用体验**：实时搜索，无需维护索引
- **改名体验**：从手动命令到自然对话
- **整体理念**：充分利用 Claude Code 的能力，而非依赖外部工具

---

## [2.0.0] - 2025-11-17

### 🚀 重大改进：零配置自动安装

**核心变化**：
- 用户只需复制 `remembering-anything` 文件夹到 `~/.claude/skills/`
- 首次运行时自动完成所有初始化工作
- 完全移除对 `~/.claude/commands/` 的依赖

### ✨ 新增功能

#### 1. 自动环境初始化
- **自动检测**：首次运行时自动检测是否存在虚拟环境
- **自动安装**：静默创建 `.venv` 并安装所有依赖
- **自动配置**：初始化目录结构和配置文件
- **友好提示**：安装完成后以自然方式打招呼

#### 2. 基于 name + description 的双重触发
- **SKILL.md 的 `name` 字段**：设置为 AI 名字（如"夏弥"）
- **SKILL.md 的 `description` 字段**：包含触发关键词
- **双重匹配**：提高 Claude 自动激活的成功率
- **智能判断**：区分"呼唤"和"讨论"

#### 3. 简化的名字管理
- `name_manager.py` 同时更新 `name` 和 `description` 字段
- 一条命令完成所有配置：`python scripts/name_manager.py set 新名字`
- 删除了 slash command 生成逻辑（不再需要）

### 🗑️ 移除功能

- **移除 slash commands 依赖**：
  - 不再生成 `~/.claude/commands/{name}.md` 文件
  - 完全基于 SKILL.md 的 metadata 触发
  - 用户无需配置任何额外文件

- **简化 name_manager.py**：
  - 移除 `generate_slash_command()` 函数
  - 移除 `remove_old_command()` 函数
  - 只保留核心的 `update_skill_metadata()` 函数

### 📝 文档更新

#### 新增文档
- **INSTALL.md**：3 步快速安装指南
- **EXAMPLE.md**：完整的使用场景示例

#### 更新文档
- **README.md**：
  - 顶部添加醒目的"快速开始"部分
  - 简化安装说明为 3 步
  - 强调零配置和自动初始化

- **CLAUDE.md**：
  - 添加核心特性说明
  - 更新开发环境设置说明
  - 明确自动安装和手动安装的区别

- **SKILL.md**：
  - 添加详细的自动初始化流程
  - 更新触发方式说明
  - 优化首次见面的话术示例

### 🔧 技术改进

#### 安装流程
**之前**：
```bash
1. 复制文件夹
2. 创建虚拟环境
3. 激活虚拟环境
4. 安装依赖
5. 初始化目录
6. 创建 slash command
7. 使用
```

**现在**：
```bash
1. 复制文件夹
2. 说"夏弥在吗"
3. 等待 30 秒
4. 完成！
```

#### 触发机制
**之前**：
```
用户 → /夏弥 → ~/.claude/commands/夏弥.md → /skill claude-memory → 激活
```

**现在**：
```
用户 → "夏弥在吗" → Claude 匹配 SKILL.md (name + description) → 激活
```

### 🎯 用户体验提升

- **安装时间**：从 5 分钟（手动）→ 30 秒（自动）
- **安装步骤**：从 7 步 → 2 步
- **出错率**：显著降低（无需手动配置）
- **文档复杂度**：大幅简化

### ⚠️ 破坏性变更

#### 对现有用户
如果你之前已经安装过旧版本：

1. **删除旧的 slash command**（可选）：
   ```bash
   rm ~/.claude/commands/夏弥.md
   # 或你之前设置的其他名字
   ```

2. **更新 SKILL.md**：
   ```bash
   cd ~/.claude/skills/remembering-anything
   python scripts/name_manager.py set 夏弥
   # 或你喜欢的名字
   ```

3. **使用新方式唤醒**：
   ```
   夏弥在吗
   ```

#### 对开发者
- `name_manager.py` 的 API 变化：
  - `generate_slash_command()` 已移除
  - `remove_old_command()` 已移除
  - 新增 `update_skill_metadata()` 函数

### 🐛 Bug 修复

- 修复 Windows 终端编码问题（UTF-8）
- 改进跨平台路径处理

### 📊 性能优化

- 首次安装使用 `pip install --quiet` 减少输出
- 自动初始化在后台静默完成

---

## [1.0.0] - 2025-11-15

### 初始版本

- 三层记忆架构（结构化记忆 + 原始笔记 + 智能总结）
- 用户画像和 AI 画像系统
- 向量检索功能
- 记忆版本控制和冲突检测
- Slash command 唤醒方式
