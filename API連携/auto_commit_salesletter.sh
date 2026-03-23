#!/bin/bash
DATE=$(date +%Y-%m-%d)
TODAY_DISPLAY=$(date +"%Y年%m月%d日")
cd ~/Desktop/AI経営本部

echo "【マスターファイルを更新中...】"
python3 ~/Desktop/AI経営本部/API連携/update_master_salesletter.py

CHANGES=$(git status --porcelain AI活用講義/セールスレター制作/)
if [ -n "$CHANGES" ]; then
    git add AI活用講義/セールスレター制作/
    git commit -m "${DATE} セールスレター更新 - ${TODAY_DISPLAY}分追加"
    git push origin salesletter-development
    echo "✅ ${TODAY_DISPLAY}のブレインダンプをGitHubに保存しました"
    echo "✅ MASTERファイルに自動追記完了"
    echo "📄 確認：https://github.com/koumeisanada/ai-keiei-honbu/blob/salesletter-development/AI活用講義/セールスレター制作/MASTER_セールスレター.md"
else
    echo "本日の変更なし"
fi
