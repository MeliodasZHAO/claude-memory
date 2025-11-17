# 快速安装指南

## 3 步完成安装

### 步骤 1：复制文件夹

```bash
# 克隆或下载这个项目
git clone https://github.com/your-repo/claude-memory.git

# 只需要复制 remembering-anything 文件夹到 Claude skills 目录
cp -r claude-memory/remembering-anything ~/.claude/skills/
```

**Windows 用户**：
```cmd
xcopy /E /I claude-memory\remembering-anything %USERPROFILE%\.claude\skills\remembering-anything
```

### 步骤 2：在 Claude Code 中唤醒

打开 Claude Code，输入：
```
夏弥在吗
```

### 步骤 3：等待自动初始化

- 首次运行会自动创建虚拟环境（几秒钟）
- 完成后 AI 会自然地打招呼
- 就这样，安装完成了！无需安装依赖，启动极快！

---

## 完成后你可以

**直接呼唤名字来激活**：
```
夏弥
夏弥在吗
夏弥在不在
```

**修改 AI 名字**（可选）：

对话式修改（推荐）：
```
帮我改个名字叫小白
我想叫你阿尔法
```

手动修改：
```bash
cd ~/.claude/skills/remembering-anything
python scripts/name_manager.py set 你喜欢的名字
```

---

## 常见问题

**Q: 首次运行需要多久？**
A: 只需几秒钟！无需下载模型或安装依赖包，相比之前的版本快了 10 倍以上。

**Q: 如何确认安装成功？**
A: 输入"夏弥在吗"，如果 AI 以友好的方式回应，就说明成功了。

**Q: 不喜欢"夏弥"这个名字？**
A: 直接在对话中说"帮我改个名字叫XX"，或运行 `python scripts/name_manager.py set 新名字`。

**Q: 需要安装什么依赖吗？**
A: 不需要！完全使用 Claude Code 的原生工具（Grep、Read 等），无需任何额外依赖。

---

## 更多帮助

查看 [README.md](README.md) 了解完整功能和使用方法。
