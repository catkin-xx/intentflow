@echo off
REM ============================================================================
REM IntentFlow GitHub 发布脚本 (Windows 版本)
REM 适用于新手，自动化提交流程
REM ============================================================================

echo ============================================================================
echo IntentFlow GitHub 发布脚本
echo ============================================================================
echo.

REM ============================================================================
REM 步骤 1：检查 Git 环境
REM ============================================================================

echo 步骤 1/8: 检查 Git 环境...
echo --------------------------------------------------------------------------

where git >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未检测到 Git
    echo 请先安装 Git: https://git-scm.com/downloads
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('git --version') do set GIT_VERSION=%%i
echo [OK] Git 版本: %GIT_VERSION%
echo.

REM ============================================================================
REM 步骤 2：配置 Git 身份（如果未配置）
REM ============================================================================

echo 步骤 2/8: 配置 Git 身份...
echo --------------------------------------------------------------------------

for /f "delims=" %%i in ('git config --global user.name') do set GIT_USERNAME=%%i
if "%GIT_USERNAME%"=="" (
    echo 请输入你的 GitHub 用户名:
    set /p GIT_USERNAME=
    git config --global user.name "%GIT_USERNAME%"
    echo [OK] 已配置用户名: %GIT_USERNAME%
) else (
    echo [OK] 用户名已配置: %GIT_USERNAME%
)

for /f "delims=" %%i in ('git config --global user.email') do set GIT_EMAIL=%%i
if "%GIT_EMAIL%"=="" (
    echo 请输入你的 GitHub 邮箱:
    set /p GIT_EMAIL=
    git config --global user.email "%GIT_EMAIL%"
    echo [OK] 已配置邮箱: %GIT_EMAIL%
) else (
    echo [OK] 邮箱已配置: %GIT_EMAIL%
)
echo.

REM ============================================================================
REM 步骤 3：初始化 Git 仓库（如果未初始化）
REM ============================================================================

echo 步骤 3/8: 初始化 Git 仓库...
echo --------------------------------------------------------------------------

if not exist ".git" (
    git init
    echo [OK] Git 仓库初始化完成
) else (
    echo [OK] Git 仓库已存在
)
echo.

REM ============================================================================
REM 步骤 4：添加所有文件
REM ============================================================================

echo 步骤 4/8: 添加文件到暂存区...
echo --------------------------------------------------------------------------

git add .
echo [OK] 所有文件已添加到暂存区
echo.
git status --short
echo.

REM ============================================================================
REM 步骤 5：创建 .gitignore（如果不存在）
REM ============================================================================

echo 步骤 5/8: 创建 .gitignore...
echo --------------------------------------------------------------------------

if not exist ".gitignore" (
    (
        echo # Python
        echo __pycache__/
        echo *.py[cod]
        echo *$py.class
        echo *.so
        echo .Python
        echo build/
        echo develop-eggs/
        echo dist/
        echo downloads/
        echo eggs/
        echo .eggs/
        echo lib/
        echo lib64/
        echo parts/
        echo sdist/
        echo var/
        echo wheels/
        echo *.egg-info/
        echo .installed.cfg
        echo *.egg
        echo.
        echo # Virtual environments
        echo venv/
        echo ENV/
        echo env/
        echo.
        echo # IDE
        echo .vscode/
        echo .idea/
        echo *.swp
        echo *.swo
        echo *~
        echo.
        echo # OS
        echo .DS_Store
        echo Thumbs.db
        echo.
        echo # Testing
        echo .pytest_cache/
        echo .coverage
        echo htmlcov/
        echo.
        echo # Documentation
        echo docs/_build/
    ) > .gitignore
    echo [OK] .gitignore 文件已创建
    git add .gitignore
) else (
    echo [OK] .gitignore 文件已存在
)
echo.

REM ============================================================================
REM 步骤 6：提交更改
REM ============================================================================

echo 步骤 6/8: 提交更改...
echo --------------------------------------------------------------------------

git commit -m "Initial release: IntentFlow v1.0.0 - Multimodal agent orchestration framework" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [警告] 没有需要提交的更改
    echo 如果你已经提交过了，请继续下一步
) else (
    echo [OK] 更改已提交
)
echo.

REM ============================================================================
REM 步骤 7：关联远程仓库
REM ============================================================================

echo 步骤 7/8: 关联远程仓库...
echo --------------------------------------------------------------------------

git remote get-url origin >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] 远程仓库已关联
    git remote get-url origin
    echo.
    set /p CHANGE_REPO="是否要更换远程仓库? (y/N): "
    if /i "%CHANGE_REPO%"=="y" (
        echo 请输入你的 GitHub 仓库地址 (格式: https://github.com/yourusername/intentflow.git):
        set /p REPO_URL=
        git remote set-url origin "%REPO_URL%"
        echo [OK] 远程仓库已更新: %REPO_URL%
    )
) else (
    echo 请输入你的 GitHub 仓库地址 (格式: https://github.com/yourusername/intentflow.git):
    set /p REPO_URL=
    git remote add origin "%REPO_URL%"
    echo [OK] 远程仓库已关联: %REPO_URL%
)
echo.

REM ============================================================================
REM 步骤 8：推送到 GitHub
REM ============================================================================

echo 步骤 8/8: 推送到 GitHub...
echo --------------------------------------------------------------------------

git ls-remote --heads origin main >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo 检测到远程 main 分支已存在
    echo 执行: git push origin main
) else (
    echo 检测到远程 main 分支不存在
    echo 执行: git push -u origin main (首次推送)
)

echo.
echo 准备推送...
echo 如果提示输入密码，请输入你的 GitHub Personal Access Token (PAT)
echo 获取 PAT: https://github.com/settings/tokens
echo.
pause

git ls-remote --heads origin main >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    git push origin main
) else (
    git push -u origin main
)

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] 推送完成！
    echo.
) else (
    echo.
    echo [错误] 推送失败
    echo 请检查网络连接和凭据
    echo.
    pause
    exit /b 1
)

REM ============================================================================
REM 完成
REM ============================================================================

echo ============================================================================
echo [OK] IntentFlow 已成功发布到 GitHub！
echo ============================================================================
echo.
echo 下一步操作:
echo 1. 访问你的仓库: （在浏览器中打开上面显示的地址）
echo 2. 检查 README.md 显示是否正常
echo 3. 验证所有文件都已上传
echo 4. 考虑添加 CI/CD 配置
echo.
echo 需要帮助？
echo   - 文档: IntentFlow_User_Guide.md
echo   - 演示文稿: IntentFlow_Slides.html
echo   - 贡献指南: CONTRIBUTING.md
echo.
echo 感谢你使用 IntentFlow！
echo.
pause
