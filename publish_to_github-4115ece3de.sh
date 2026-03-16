#!/bin/bash

################################################################################
# IntentFlow GitHub 发布脚本
# 适用于新手，自动化提交流程
################################################################################

set -e  # 遇到错误立即退出

echo "=========================================================================="
echo "IntentFlow GitHub 发布脚本"
echo "=========================================================================="
echo ""

################################################################################
# 步骤 1：检查环境
################################################################################

echo "步骤 1/8: 检查 Git 环境..."
echo "--------------------------------------------------------------------------"

# 检查 Git 是否安装
if ! command -v git &> /dev/null; then
    echo "❌ 错误: 未检测到 Git"
    echo "请先安装 Git: https://git-scm.com/downloads"
    exit 1
fi

GIT_VERSION=$(git --version)
echo "✓ Git 版本: $GIT_VERSION"
echo ""

################################################################################
# 步骤 2：配置 Git 身份（如果未配置）
################################################################################

echo "步骤 2/8: 配置 Git 身份..."
echo "--------------------------------------------------------------------------"

# 检查是否已配置
if [ -z "$(git config --global user.name)" ]; then
    echo "请输入你的 GitHub 用户名:"
    read -r GIT_USERNAME
    git config --global user.name "$GIT_USERNAME"
    echo "✓ 已配置用户名: $GIT_USERNAME"
else
    echo "✓ 用户名已配置: $(git config --global user.name)"
fi

if [ -z "$(git config --global user.email)" ]; then
    echo "请输入你的 GitHub 邮箱:"
    read -r GIT_EMAIL
    git config --global user.email "$GIT_EMAIL"
    echo "✓ 已配置邮箱: $GIT_EMAIL"
else
    echo "✓ 邮箱已配置: $(git config --global user.email)"
fi
echo ""

################################################################################
# 步骤 3：初始化 Git 仓库（如果未初始化）
################################################################################

echo "步骤 3/8: 初始化 Git 仓库..."
echo "--------------------------------------------------------------------------"

if [ ! -d ".git" ]; then
    git init
    echo "✓ Git 仓库初始化完成"
else
    echo "✓ Git 仓库已存在"
fi
echo ""

################################################################################
# 步骤 4：添加所有文件
################################################################################

echo "步骤 4/8: 添加文件到暂存区..."
echo "--------------------------------------------------------------------------"

git add .
echo "✓ 所有文件已添加到暂存区"
echo ""
git status --short
echo ""

################################################################################
# 步骤 5：创建 .gitignore（如果不存在）
################################################################################

echo "步骤 5/8: 创建 .gitignore..."
echo "--------------------------------------------------------------------------"

if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Documentation
docs/_build/
EOF
    echo "✓ .gitignore 文件已创建"
    git add .gitignore
else
    echo "✓ .gitignore 文件已存在"
fi
echo ""

################################################################################
# 步骤 6：提交更改
################################################################################

echo "步骤 6/8: 提交更改..."
echo "--------------------------------------------------------------------------"

COMMIT_MESSAGE="Initial release: IntentFlow v1.0.0 - Multimodal agent orchestration framework

Features:
- Intent-driven architecture with adaptive routing
- Native multimodal support (text, image, audio, video)
- Agent collaboration mechanism
- Full observability with telemetry system
- Workflow DSL for complex orchestrations
- Complete documentation and examples"

git commit -m "$COMMIT_MESSAGE" || {
    echo "⚠️  警告: 没有需要提交的更改"
    echo "如果你已经提交过了，请继续下一步"
}
echo "✓ 更改已提交"
echo ""

################################################################################
# 步骤 7：关联远程仓库
################################################################################

echo "步骤 7/8: 关联远程仓库..."
echo "--------------------------------------------------------------------------"

# 检查是否已关联远程仓库
if git remote get-url origin &> /dev/null; then
    echo "✓ 远程仓库已关联: $(git remote get-url origin)"
    echo ""
    read -p "是否要更换远程仓库? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "请输入你的 GitHub 仓库地址 (格式: https://github.com/yourusername/intentflow.git):"
        read -r REPO_URL
        git remote set-url origin "$REPO_URL"
        echo "✓ 远程仓库已更新: $REPO_URL"
    fi
else
    echo "请输入你的 GitHub 仓库地址 (格式: https://github.com/yourusername/intentflow.git):"
    read -r REPO_URL

    # 验证 URL 格式
    if [[ ! $REPO_URL =~ ^https://github\.com/.*\.git$ ]]; then
        echo "⚠️  警告: URL 格式可能不正确，但继续执行..."
    fi

    git remote add origin "$REPO_URL"
    echo "✓ 远程仓库已关联: $REPO_URL"
fi
echo ""

################################################################################
# 步骤 8：推送到 GitHub
################################################################################

echo "步骤 8/8: 推送到 GitHub..."
echo "--------------------------------------------------------------------------"

# 检查远程分支是否存在
if git ls-remote --heads origin main &> /dev/null; then
    echo "检测到远程 main 分支已存在"
    echo "执行: git push origin main"
else
    echo "检测到远程 main 分支不存在"
    echo "执行: git push -u origin main (首次推送)"
fi

echo ""
echo "准备推送..."
echo "如果提示输入密码，请输入你的 GitHub Personal Access Token (PAT)"
echo "获取 PAT: https://github.com/settings/tokens"
echo ""

read -p "按回车键继续，或 Ctrl+C 取消..." -r

if git ls-remote --heads origin main &> /dev/null; then
    git push origin main
else
    git push -u origin main
fi

echo ""
echo "✓ 推送完成！"
echo ""

################################################################################
# 完成
################################################################################

echo "=========================================================================="
echo "✓ IntentFlow 已成功发布到 GitHub！"
echo "=========================================================================="
echo ""
echo "下一步操作:"
echo "1. 访问你的仓库: $(git remote get-url origin | sed 's/\.git$//')"
echo "2. 检查 README.md 显示是否正常"
echo "3. 验证所有文件都已上传"
echo "4. 考虑添加 CI/CD 配置"
echo ""
echo "需要帮助？"
echo "  - 文档: IntentFlow_User_Guide.md"
echo "  - 演示文稿: IntentFlow_Slides.html"
echo "  - 贡献指南: CONTRIBUTING.md"
echo ""
echo "感谢你使用 IntentFlow！🚀"
echo ""
