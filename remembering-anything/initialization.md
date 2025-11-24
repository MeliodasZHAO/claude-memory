# 初始化和环境设置

本文档详细说明首次运行时的自动初始化流程。

## 自动初始化流程

### 检测环境

系统会检查虚拟环境是否存在：

```bash
# 检查 .venv 目录
if [ ! -d "~/.claude/skills/remembering-anything/.venv" ]; then
    echo "first_run"  # 需要初始化
else
    echo "initialized"  # 已经初始化
fi
```

### 首次运行设置

如果是首次运行，系统会自动：

1. **创建虚拟环境**
   ```bash
   cd ~/.claude/skills/remembering-anything
   python -m venv .venv
   ```

2. **安装依赖**（如果有 requirements.txt）
   ```bash
   # Windows
   .venv/Scripts/python.exe -m pip install --quiet -r scripts/requirements.txt

   # macOS/Linux
   .venv/bin/python -m pip install --quiet -r scripts/requirements.txt
   ```

3. **初始化目录结构**
   ```bash
   python scripts/setup_directories.py
   ```

### 目录结构

初始化后会创建以下目录：

```
user-data/
├── memory/           # 结构化记忆
│   ├── facts.json
│   ├── preferences.json
│   ├── experiences.json
│   └── .quick_load_cache.json
├── notes/           # 原始笔记
│   ├── daily/
│   ├── topics/
│   └── projects/
├── summaries/       # AI 总结
│   ├── monthly/
│   └── topics/
├── config/          # 配置文件
│   ├── user-persona.md
│   └── ai-persona.md
├── media/           # 媒体文件
│   └── images/
├── outputs/         # 临时输出
└── backups/         # 备份文件
```

## 配置文件加载顺序

### 首次见面

1. 检查 `user-data/config/user-persona.md` 是否存在
2. 如果不存在 → 进入首次见面模式
3. 从 `~/.claude/CLAUDE.md` 读取全局 AI 画像
4. 如果没有全局画像，使用默认模板

### 日常激活

1. **快速加载核心记忆**
   - 运行 `quick_load.py` 脚本
   - 读取 `.quick_load_cache.json`

2. **读取配置**
   - `user-data/config/user-persona.md` - 用户画像
   - 从缓存中获取核心记忆

3. **按需加载**
   - 根据对话内容加载相关记忆
   - 使用 Grep 搜索笔记

## Python 环境要求

- Python 3.8 或更高版本
- 支持 Windows、macOS、Linux
- 无需额外依赖包（使用标准库）

## 路径配置

所有脚本使用 `path_config.py` 模块管理路径：

```python
from path_config import get_user_data_dir

# 自动获取正确的 user-data 路径
user_data = get_user_data_dir()
```

开发环境和运行环境会自动切换路径。

## 编码处理

所有文件操作使用 UTF-8 编码：

```python
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
```

## 错误处理

初始化过程中的错误会被简化为用户友好的提示：

- ✅ "唔...好像卡住了"
- ❌ "虚拟环境创建失败: Permission denied"

## 重要原则

1. **完全静默** - 初始化过程不向用户汇报
2. **自动完成** - 无需用户干预
3. **快速启动** - 优化加载速度
4. **容错设计** - 缺失文件自动创建