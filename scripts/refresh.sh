#!/usr/bin/env bash
# ============================================================
#  晨间信息流 - 手动刷新一键脚本（Git Bash / WSL / macOS / Linux）
#  流程: 跑生成脚本 -> 有变化则 commit -> push -> Cloudflare 自动部署
#  用法: bash scripts/refresh.sh
#  依赖: python3 + git（GitHub 凭据已配置）
# ============================================================
set -e
cd "$(dirname "$0")/.."

echo "[1/4] 正在抓取并生成晨报..."
PY=python3
command -v python3 >/dev/null 2>&1 || PY=python
$PY scripts/daily_brief.py

echo "[2/4] 暂存变更..."
git add public/morning/index.html scripts/daily_brief.py 2>/dev/null || true

echo "[3/4] 提交并推送..."
if git diff --cached --quiet; then
    echo "[INFO] 内容无变化，跳过提交。"
else
    git commit -m "daily brief update (manual)"
    git push origin main
fi

echo "[4/4] 完成。约 1-2 分钟后 Cloudflare 自动部署。"
echo "      验证: https://enki-yan.pages.dev/morning/"
