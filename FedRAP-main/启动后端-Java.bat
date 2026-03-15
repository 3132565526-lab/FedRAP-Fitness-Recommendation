@echo off
chcp 65001
echo ========================================
echo FedRAP 智能健身推荐系统 - 后端启动脚本
echo ========================================
echo.

cd /d "%~dp0backend-java"

echo 检查运行环境...
echo.

REM 检查是否有 Maven Wrapper
if exist "mvnw.cmd" (
    echo 使用 Maven Wrapper 启动（无需安装Maven）...
    echo.
    echo 正在启动后端服务器...
    echo 端口: 8080
    echo API 地址: http://localhost:8080/api
    echo H2 控制台: http://localhost:8080/api/h2-console
    echo.
    call mvnw.cmd spring-boot:run
    goto :end
)

REM 检查系统是否安装了 Maven
where mvn >nul 2>nul
if %errorlevel% equ 0 (
    echo 使用系统 Maven 启动...
    echo.
    echo 正在启动后端服务器...
    echo 端口: 8080
    echo API 地址: http://localhost:8080/api
    echo H2 控制台: http://localhost:8080/api/h2-console
    echo.
    mvn spring-boot:run
    goto :end
)

REM 都没有，给出提示
echo [错误] 未检测到 Maven 或 Maven Wrapper
echo.
echo 解决方案：
echo 1. 运行 "安装Maven-Wrapper.bat" 脚本（推荐）
echo 2. 或安装 Maven: https://maven.apache.org/download.cgi
echo.
pause
exit /b 1

:end
pause
