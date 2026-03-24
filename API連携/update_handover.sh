#!/bin/bash
# 引き継ぎマスターファイルを最新状態に自動更新するスクリプト
# 実行：bash ~/Desktop/AI経営本部/API連携/update_handover.sh

TODAY=$(date '+%Y年%m月%d日')
HANDOVER_FILE="$HOME/Desktop/AI経営本部/SKILL_引き継ぎマスター.md"

# 最終更新日を更新
sed -i '' "s/# 最終更新：.*/# 最終更新：$TODAY/" "$HANDOVER_FILE"

# 最新のセールスレターバージョンを確認
LATEST_SL=$(ls ~/Desktop/AI経営本部/AI活用講義/セールスレター制作/09_最終完成/ | grep "完全版" | sort | tail -1)
echo "最新セールスレター：$LATEST_SL"

# GitHubにプッシュ
cd ~/Desktop/AI経営本部
git add SKILL_引き継ぎマスター.md
git commit -m "引き継ぎマスター更新：$TODAY"
git push origin main

echo "✅ 引き継ぎマスター更新完了：$TODAY"
