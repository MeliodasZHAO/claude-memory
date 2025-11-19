# 开发指南

## 核心理念

**简单优先**：用户只需要一个 `remembering-anything/` 目录，所有数据在 `user-data/` 里。

## 目录结构

```
~/.claude/skills/
├── claude-memory/                     # Git 项目（你的开发环境）
│   └── remembering-anything/
│       ├── assets/                    # 需要发布
│       ├── scripts/                   # 需要发布
│       │   └── path_config.py         # 路径管理核心
│       ├── SKILL.md                   # 需要发布
│       └── user-data/                 # 本地测试用（.gitignore）
│
└── remembering-anything/              # 用户的运行环境
    ├── assets/
    ├── scripts/
    ├── SKILL.md
    └── user-data/                     # 真实用户数据
```

## 开发流程

### 1. 日常开发

在 `claude-memory/remembering-anything/` 中修改代码：
- 编辑 `scripts/*.py`
- 更新 `SKILL.md`
- 修改 `assets/` 模板

### 2. 路径管理

**所有脚本都使用 `path_config.py`**：

```python
from path_config import get_user_data_dir, get_memory_dir

# 自动获取正确路径
user_data = get_user_data_dir()
memory_dir = get_memory_dir()
```

`path_config.py` 会自动检测环境：
- 开发环境：指向 `~/.claude/skills/remembering-anything/user-data/`
- 运行环境：使用相对路径 `../user-data/`

### 3. 测试

开发环境的脚本直接操作运行环境的数据，无需手动复制：

```bash
cd ~/.claude/skills/claude-memory/remembering-anything/scripts
python memory_visualizer.py
# ✓ 文件生成在 ~/.claude/skills/remembering-anything/user-data/outputs/
```

### 4. 提交代码

```bash
cd ~/.claude/skills/claude-memory
git add .
git commit -m "feat: 你的改动"
git push
```

**注意**：`.gitignore` 已排除 `user-data/`，不会上传用户数据。

### 5. 发布更新

用户更新时，只需要同步三个部分：
- `assets/`
- `scripts/`
- `SKILL.md`

用户的 `user-data/` 不会被覆盖，保留所有记忆数据。

## 添加新脚本

创建新脚本时，使用路径配置模块：

```python
#!/usr/bin/env python3
"""
我的新脚本
"""
from path_config import get_user_data_dir, get_memory_dir

def main():
    # 自动适配开发/运行环境
    memory_dir = get_memory_dir()
    # ... 你的逻辑

if __name__ == "__main__":
    main()
```

## 常见问题

### Q: 为什么开发环境的脚本要指向运行环境的数据？

A: 这样可以直接在真实环境测试，避免：
- 维护两份数据
- 手动复制数据
- 数据不同步的问题

### Q: 如果我想在开发环境有独立的测试数据怎么办？

A: 临时修改 `path_config.py` 中的 `is_dev_env` 检测逻辑，让它返回 False 即可。

### Q: 发布时需要做什么？

A: 只需要复制三个文件夹（assets/scripts/SKILL.md）到发布位置，用户的 user-data 自动保留。

## 未来：版本迁移

如果 `user-data` 结构变化（如新增字段、重命名文件），需要：

1. 在 SKILL.md 中声明版本号
2. 创建 `scripts/migrations/v1_to_v2.py` 迁移脚本
3. 在 skill 激活时自动检测版本并执行迁移

这部分功能待实现。
