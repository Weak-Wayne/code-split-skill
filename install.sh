#!/bin/bash

# Code Split Skill - 安装脚本
# 支持 GitHub 一键安装

SKILL_NAME="code-split-skill"
SKILL_DIR="$HOME/.trae/skills/$SKILL_NAME"

echo "=========================================="
echo "  代码模块化拆分技能安装"
echo "=========================================="

# 检查是否已安装
if [ -d "$SKILL_DIR" ]; then
    echo "[INFO] 检测到已安装，正在更新..."
    rm -rf "$SKILL_DIR"
fi

# 创建技能目录
mkdir -p "$SKILL_DIR"

# 复制技能文件
cp skill.json "$SKILL_DIR/"
cp prompt.md "$SKILL_DIR/"
cp README.md "$SKILL_DIR/"

echo "[INFO] 技能文件已复制到: $SKILL_DIR"
echo ""
echo "[SUCCESS] 安装完成！"
echo ""
echo "使用方式："
echo "1. 在IDE中触发技能（输入：帮我写代码、创建项目等）"
echo "2. 技能会自动提示进行模块功能分析"
echo "3. 按照分析结果编写模块化代码"
echo "=========================================="