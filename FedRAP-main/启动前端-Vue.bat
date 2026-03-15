@echo off
chcp 65001
echo ========================================
echo FedRAP 智能健身推荐系统 - 前端启动脚本
echo ========================================
echo.

cd /d "%~dp0frontend-vue"

echo 检查 Node.js 是否安装...
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Node.js
    echo.
    echo Node.js 是运行前端必需的环境，请先安装：
    echo.
    echo 下载地址: https://nodejs.org/
    echo 推荐版本: 18.x LTS 或 20.x LTS
    echo.
    echo 安装步骤：
    echo 1. 访问上面的网址下载 Node.js 安装包
    echo 2. 运行安装程序（一路点击"下一步"即可）
    echo 3. 安装完成后重启命令行窗口
    echo 4. 重新运行此脚本
    echo.
    echo 验证安装: 打开新命令行输入 node -v
    echo.
    pause
    exit /b 1
)

echo.
echo 检查依赖是否已安装...
if not exist "node_modules" (
    echo 首次运行，正在安装依赖...
    call npm install
    if %errorlevel% neq 0 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)

echo.
echo 正在启动前端开发服务器...
echo 地址: http://localhost:5173
echo.

npm run dev

pause
