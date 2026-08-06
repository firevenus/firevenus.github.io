@echo off
REM ============================================================
REM  晨间信息流 - 手动刷新一键脚本（双击即用）
REM  流程: 跑生成脚本 -> 有变化则 commit -> push -> Cloudflare 自动部署
REM  注意: 需已安装 Python 3 (PATH 或 py launcher) 与 Git
REM ============================================================
chcp 65001 >nul
setlocal
cd /d "%~dp0.."

REM --- 探测 Python ---
set PY=python
where python >nul 2>nul
if errorlevel 1 (
    where py >nul 2>nul
    if errorlevel 1 (
        echo [FAIL] 未找到 Python。请安装 Python 3 并加入 PATH。
        pause
        exit /b 1
    )
    set PY=py -3
)

echo [1/4] 正在抓取并生成晨报...
%PY% scripts\daily_brief.py
if errorlevel 1 (
    echo [FAIL] 生成失败，请检查网络或脚本错误。
    pause
    exit /b 1
)

echo [2/4] 暂存变更...
git add public/morning/index.html scripts/daily_brief.py >nul 2>nul

echo [3/4] 提交并推送...
git commit -m "daily brief update (manual)" >nul 2>nul
if errorlevel 1 (
    echo [INFO] 内容无变化，跳过提交。
) else (
    git push origin main
    if errorlevel 1 (
        echo [FAIL] 推送失败，请检查 Git 凭据/网络。
        pause
        exit /b 1
    )
)

echo [4/4] 完成。约 1-2 分钟后 Cloudflare 自动部署。
echo       验证: https://enki-yan.pages.dev/morning/
pause
