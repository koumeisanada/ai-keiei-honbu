#!/bin/bash
# ===========================================
# cron用ラッパースクリプト
# 毎朝6:00に自動実行される
# ===========================================

# PATHを設定（cronはPATHが限定的なため）
export PATH="/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin:$HOME/.nvm/versions/node/$(ls $HOME/.nvm/versions/node/ 2>/dev/null | tail -1)/bin:$PATH"

# Homebrewのパスを追加（Apple Silicon Mac用）
if [ -f /opt/homebrew/bin/brew ]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# .zshrcからAPIキー等の環境変数を読み込む
if [ -f "$HOME/.zshrc" ]; then
    source <(grep '^export ' "$HOME/.zshrc")
fi

# HOMEを明示的に設定
export HOME="/Users/sanadahiroaki"

# パイプライン実行
bash "$HOME/Desktop/AI経営本部/API連携/pipeline_daily.sh"
