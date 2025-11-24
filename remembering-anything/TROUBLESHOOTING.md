# 故障排除指南

遇到问题？这里收集了常见问题和解决方案。

---

## Python 环境问题

### "python" 命令找不到

**症状**：
```
'python' is not recognized as an internal or external command
```

**解决方案**：

1. **Windows**：尝试使用 `python3` 或 `py`
   ```bash
   py scripts/activate.py
   ```

2. **检查 Python 是否安装**：
   ```bash
   python --version
   # 或
   python3 --version
   ```

3. **确保 Python 在 PATH 中**：重新安装 Python 时勾选 "Add Python to PATH"

---

### 虚拟环境问题

**症状**：脚本报错找不到模块

**解决方案**：

```bash
# 进入 skill 目录
cd ~/.claude/skills/remembering-anything

# 创建虚拟环境（如果不存在）
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 安装依赖（如果有 requirements.txt）
pip install -r scripts/requirements.txt
```

---

## 编码问题

### 中文显示乱码

**症状**：输出显示为 `\u4e2d\u6587` 或乱码

**解决方案**：

1. **设置环境变量**：
   ```bash
   # Windows PowerShell
   $env:PYTHONIOENCODING="utf-8"

   # Windows CMD
   set PYTHONIOENCODING=utf-8

   # macOS/Linux
   export PYTHONIOENCODING=utf-8
   ```

2. **永久解决（Windows）**：
   - 系统属性 → 高级 → 环境变量
   - 添加用户变量：`PYTHONIOENCODING` = `utf-8`

---

### JSON 文件读取失败

**症状**：
```
UnicodeDecodeError: 'gbk' codec can't decode byte...
```

**原因**：文件编码不是 UTF-8

**解决方案**：
1. 用文本编辑器打开文件，另存为 UTF-8 编码
2. 或者删除文件让系统重新生成

---

## 首次运行问题

### 目录结构不存在

**症状**：脚本报错找不到 `user-data` 目录

**解决方案**：

```bash
# 运行初始化脚本
python scripts/setup_directories.py
```

这会创建完整的目录结构：
```
user-data/
├── notes/
│   ├── daily/
│   ├── topics/
│   └── projects/
├── memory/
│   ├── facts.json
│   ├── preferences.json
│   └── experiences.json
├── summaries/
│   ├── monthly/
│   └── topics/
├── config/
└── outputs/
```

---

### 缓存文件不存在

**症状**：
```
FileNotFoundError: .quick_load_cache.json
```

**解决方案**：

```bash
# 运行激活脚本生成缓存
python scripts/activate.py
```

---

## 记忆相关问题

### 记忆没有保存

**可能原因**：

1. **暂存区没有提交**
   ```bash
   # 检查暂存区
   python scripts/memory_staging.py list

   # 提交记忆
   python scripts/memory_staging.py commit
   ```

2. **JSON 文件损坏**
   - 检查 `user-data/memory/*.json` 文件格式是否正确
   - 可以删除损坏的文件让系统重新创建空文件

---

### 记忆冲突

**症状**：系统检测到矛盾信息

**解决方案**：

```bash
# 查看冲突
python scripts/memory_cli.py conflicts

# 手动编辑 facts.json/preferences.json 解决冲突
# 将旧记忆的 status 改为 "deprecated"
```

---

### 宠物/人物信息显示错误

**可能原因**：缓存过期

**解决方案**：

```bash
# 删除缓存文件
rm user-data/memory/.quick_load_cache.json

# 重新生成
python scripts/activate.py
```

---

## 项目记忆问题

### 项目 ID 检测错误

**症状**：项目被识别为错误的 ID

**解决方案**：

1. **在 CLAUDE.md 中手动指定**：
   ```markdown
   project_id: owner/repo
   ```

2. **检查 git remote**：
   ```bash
   git remote get-url origin
   ```

---

### 项目记忆没有加载

**可能原因**：项目 ID 变化导致无法匹配

**解决方案**：

1. 检查 `user-data/memory/projects/` 目录下的文件夹名
2. 确认项目 ID 格式（`/` 会被替换为 `__`）

---

## 性能问题

### 激活速度慢

**可能原因**：缓存每次都重新生成

**优化方案**：
- activate.py 默认会检查缓存新鲜度（5 分钟内直接使用）
- 如果仍然慢，检查笔记数量是否过多

---

### 搜索结果不准确

**原因**：Grep 只支持关键词匹配，不支持语义搜索

**建议**：
1. 使用更精确的关键词
2. 尝试多个同义词搜索
3. 如果找不到，诚实告诉用户

---

## 平台特定问题

### Windows 路径问题

**症状**：路径中的 `\` 导致错误

**解决方案**：
- 使用 `/` 代替 `\`
- 或使用原始字符串：`r"C:\path\to\file"`

---

### macOS 权限问题

**症状**：
```
Permission denied
```

**解决方案**：

```bash
# 添加执行权限
chmod +x scripts/*.py
```

---

## 获取帮助

如果以上方案都无法解决问题：

1. **检查日志**：查看脚本输出的错误信息
2. **查看文档**：
   - [WORKFLOWS.md](WORKFLOWS.md) - 详细工作流
   - [memory-system.md](memory-system.md) - 系统架构
3. **提交 Issue**：[GitHub Issues](https://github.com/your-repo/claude-memory/issues)

---

## 常用诊断命令

```bash
# 检查 Python 版本
python --version

# 检查目录结构
ls -la user-data/

# 查看记忆统计
python scripts/memory_cli.py stats

# 检查缓存文件
cat user-data/memory/.quick_load_cache.json

# 检查暂存区
python scripts/memory_staging.py list
```
