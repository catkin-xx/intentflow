# IntentFlow GitHub 发布操作指南

**专为新手设计的保姆级教程**

---

## 📋 准备工作

### 1. 检查当前目录

确保你当前在包含所有代码的目录下：

```bash
# 查看当前目录
pwd

# 查看文件列表
ls
```

**你应该看到这些文件**：
```
intentflow_core.py
intentflow_nodes.py
demo_intentflow.py
intentflow_advanced.py
IntentFlow_README.md
demo_advanced.py
visualize_flow.py
IntentFlow_User_Guide.md
IntentFlow_Presentation.md
generate_presentation.py
IntentFlow_Printable.md
IntentFlow_Slides.html
IntentFlow_Speaker_Notes.md
LICENSE
.github_workflows_ci.yml
README.md
CONTRIBUTING.md
setup.py
publish_to_github.sh
publish_to_github.bat
PUBLISH_GUIDE.md
```

### 2. 注册 GitHub 账号

如果还没有，请先注册：
- 访问：https://github.com/signup
- 完成注册流程

### 3. 创建 GitHub 仓库

#### 步骤详解：

1. **登录 GitHub**
   - 访问：https://github.com/login
   - 输入用户名和密码

2. **创建新仓库**
   - 点击右上角 **"+"** 图标
   - 选择 **"New repository"**

3. **填写仓库信息**
   ```
   Repository name: intentflow
   Description: Next-generation multimodal agent orchestration framework
   Public/Private: 选择 Public（开源推荐）
   ✅ Add a README file: 勾选
   ✅ Add .gitignore: 选择 Python
   ✅ Choose a license: 选择 MIT License
   ```

4. **点击"Create repository"**

5. **复制仓库地址**
   ```
   https://github.com/yourusername/intentflow.git
   ```
   **重要**：替换 `yourusername` 为你的实际用户名，并**记下这个地址**。

---

## 🚀 方法一：自动化脚本（推荐）

### Linux / macOS

```bash
# 给脚本添加执行权限
chmod +x publish_to_github.sh

# 运行脚本
./publish_to_github.sh
```

### Windows

双击运行 `publish_to_github.bat` 文件，或在命令行中：

```cmd
publish_to_github.bat
```

### 脚本会自动完成：

1. ✓ 检查 Git 环境
2. ✓ 配置 Git 身份
3. ✓ 初始化 Git 仓库
4. ✓ 添加所有文件到暂存区
5. ✓ 创建 .gitignore
6. ✓ 提交更改
7. ✓ 关联远程仓库
8. ✓ 推送到 GitHub

**你只需要**：
- 跟随提示输入信息
- 在需要时输入 GitHub Personal Access Token

---

## 🔧 方法二：手动操作（完全控制）

### 步骤 1：安装 Git

**Windows**：下载并安装 https://git-scm.com/download/win

**macOS**：终端输入 `git --version`，如果没有会提示安装

**Linux**：
```bash
sudo apt update
sudo apt install git
```

### 步骤 2：配置 Git 身份

```bash
# 配置用户名（替换为你的 GitHub 用户名）
git config --global user.name "yourusername"

# 配置邮箱（替换为你的 GitHub 邮箱）
git config --global user.email "youremail@example.com"
```

### 步骤 3：初始化 Git 仓库

```bash
# 初始化
git init

# 查看状态
git status
```

### 步骤 4：添加文件

```bash
# 添加所有文件
git add .

# 或者逐个添加
git add intentflow_core.py
git add intentflow_nodes.py
# ...（添加所有其他文件）
```

### 步骤 5：提交更改

```bash
git commit -m "Initial release: IntentFlow v1.0.0 - Multimodal agent orchestration framework"
```

### 步骤 6：关联远程仓库

**替换 `yourusername` 为你的实际用户名**：

```bash
git remote add origin https://github.com/yourusername/intentflow.git
```

**验证**：
```bash
git remote -v
```

应该看到：
```
origin  https://github.com/yourusername/intentflow.git (fetch)
origin  https://github.com/yourusername/intentflow.git (push)
```

### 步骤 7：获取 Personal Access Token（PAT）

GitHub 现在不再支持密码登录，需要使用 PAT：

1. 访问：https://github.com/settings/tokens
2. 点击 **"Generate new token"** → **"Generate new token (classic)"**
3. 填写信息：
   ```
   Note: Git Push Token
   Expiration: 90 days
   Select scopes: 勾选 repo（完整仓库权限）
   ```
4. 点击 **"Generate token"**
5. **复制 token**（只显示一次，保存好！）

### 步骤 8：推送到 GitHub

```bash
# 首次推送（会要求输入用户名和 token）
git push -u origin main
```

**当提示输入密码时**：
- 输入用户名
- 输入 **PAT**（不是你的 GitHub 密码）

### 步骤 9：验证发布成功

1. 访问你的仓库：
   ```
   https://github.com/yourusername/intentflow
   ```

2. 检查：
   - ✓ README.md 显示在首页
   - ✓ 所有文件都已上传
   - ✓ 代码高亮显示正常

---

## 🔑 常见问题

### Q1: 推送时提示 "Authentication failed"

**A**: 需要使用 Personal Access Token (PAT)，而不是密码。

获取 PAT 的步骤：
1. 访问：https://github.com/settings/tokens
2. 生成新 token
3. 复制 token
4. 推送时输入 token

### Q2: 提示 "fatal: remote origin already exists"

**A**: 远程仓库已关联，可以更新或删除：

```bash
# 查看当前远程仓库
git remote -v

# 更新远程仓库地址
git remote set-url origin https://github.com/yourusername/intentflow.git

# 或者删除后重新添加
git remote remove origin
git remote add origin https://github.com/yourusername/intentflow.git
```

### Q3: 提示 "error: failed to push some refs"

**A**: 远程仓库有文件冲突，需要先拉取：

```bash
# 拉取远程更改
git pull origin main --allow-unrelated-histories

# 如果有冲突，解决后重新提交
git add .
git commit -m "Merge remote changes"

# 再次推送
git push origin main
```

### Q4: 如何撤销错误的提交？

**A**: 如果还没推送，可以重置：

```bash
# 重置到上一个提交（保留更改）
git reset --soft HEAD~1

# 或者完全撤销上一个提交
git reset --hard HEAD~1
```

如果已经推送，需要强制推送（不推荐）：

```bash
git push --force origin main
```

### Q5: 如何查看提交历史？

```bash
# 查看提交历史
git log

# 查看简洁的历史
git log --oneline

# 查看图表化历史
git log --graph --oneline --all
```

---

## 📦 发布后检查清单

### 立即检查

- [ ] 访问仓库首页，README.md 显示正常
- [ ] 检查所有文件是否都已上传
- [ ] 点击代码文件，语法高亮正常
- [ ] 检查 LICENSE 文件是否正确显示

### 可选优化

- [ ] 添加仓库描述和标签
- [ ] 设置仓库主题（Settings → Features → Topics）
- [ ] 启用 GitHub Pages（部署演示文稿）
- [ ] 配置 CI/CD（.github/workflows/ci.yml）
- [ ] 添加项目网站链接

### 推广

- [ ] 分享到社交媒体（Twitter、LinkedIn）
- [ ] 发布到相关技术社区（Hacker News、Reddit）
- [ ] 写技术博客介绍项目
- [ ] 录制演示视频

---

## 🎯 下一步

### 1. 发布到 PyPI（可选）

```bash
# 安装构建工具
pip install build twine

# 构建
python -m build

# 上传到 PyPI
twine upload dist/*
```

### 2. 设置 GitHub Pages

1. 仓库设置：**Settings** → **Pages**
2. 选择分支：`main` → `/docs` 或 `/`
3. 访问：`https://yourusername.github.io/intentflow`

### 3. 添加 CI/CD

GitHub Actions 会自动运行 `.github/workflows/ci.yml`，每次提交都会自动测试。

---

## 🆘 获取帮助

### 文档资源

- [官方文档](https://docs.github.com/)
- [Git 教程](https://git-scm.com/docs/gittutorial)

### 社区支持

- GitHub Community: https://github.com/community
- Stack Overflow: https://stackoverflow.com/questions/tagged/git

### 联系我们

- Email: support@intentflow.dev
- Discord: https://discord.gg/intentflow

---

## ✅ 完成检查

当你完成所有步骤后，你应该能够：

1. ✓ 访问 https://github.com/yourusername/intentflow
2. ✓ 看到 README.md 和所有代码文件
3. ✓ 代码语法高亮正常
4. ✓ LICENSE 文件正确显示
5. ✓ 可以 Clone 仓库到其他地方

---

**恭喜！IntentFlow 已经成功发布到 GitHub！** 🎉

现在你可以：
- 分享仓库链接给朋友
- 在社交媒体上推广
- 开始接收社区反馈
- 继续开发新功能

**感谢你选择 IntentFlow！** 🚀
