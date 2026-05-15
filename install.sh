#!/usr/bin/env bash
# Cosle Skills 一键安装脚本
# 把 cosmo-report / prelaunch-listing / listing-image-audit 三个 skill
# 复制到 ~/.claude/skills/ 下

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${HOME}/.claude/skills"

SKILLS=("cosmo-report" "prelaunch-listing" "listing-image-audit")

echo "🎨 Cosle Skills · 安装脚本"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "源目录:   ${SCRIPT_DIR}"
echo "目标目录: ${TARGET_DIR}"
echo

# 确保目标目录存在
mkdir -p "${TARGET_DIR}"

for skill in "${SKILLS[@]}"; do
    SRC="${SCRIPT_DIR}/${skill}"
    DST="${TARGET_DIR}/${skill}"

    if [ ! -d "${SRC}" ]; then
        echo "⚠  跳过 ${skill}: 源目录不存在"
        continue
    fi

    if [ -d "${DST}" ]; then
        read -p "❓ ${skill} 已存在，覆盖？[y/N] " yn
        case $yn in
            [Yy]*) rm -rf "${DST}";;
            *) echo "   跳过"; continue;;
        esac
    fi

    cp -r "${SRC}" "${DST}"
    echo "✓ ${skill} → ${DST}"
done

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ 安装完成。在 Claude Code 中可用以下方式触发:"
echo "   /cosmo-report          已上架产品 SP Prompts 诊断"
echo "   /prelaunch-listing     新品文字 listing 预测报告"
echo "   /listing-image-audit   主图 + A+ 视觉打分诊断"
echo
echo "或用中文触发词，如 '主图打分'、'新品 listing'、'帮我分析广告报告'。"
