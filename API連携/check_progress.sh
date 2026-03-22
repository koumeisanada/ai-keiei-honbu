#!/bin/bash
echo "================================================"
echo "  AI経営本部 本日のアウトプット確認レポート"
echo "  $(date +"%Y年%m月%d日 %H:%M")"
echo "================================================"
echo ""

DATE=$(date +%Y%m%d)
DATE_HYPHEN=$(date +%Y-%m-%d)
BASE="$HOME/Desktop/AI経営本部"

echo "【集客販売 日次成果物】"
if [ -d "$BASE/集客販売/日次成果物/$DATE" ]; then
    echo "✅ フォルダあり：$DATE"
    ls "$BASE/集客販売/日次成果物/$DATE/" | while read f; do
        size=$(wc -c < "$BASE/集客販売/日次成果物/$DATE/$f")
        echo "  ✅ $f（${size}文字）"
    done
else
    echo "  ❌ 本日の成果物フォルダなし → パイプライン未実行"
fi
echo ""

echo "【米国株デイリーリサーチ】"
RESEARCH="$BASE/北の株式投資大学/資料/デイリーリサーチ"
if ls "$RESEARCH/${DATE}*.md" 2>/dev/null | head -1 | grep -q .; then
    echo "  ✅ 本日のリサーチあり"
else
    echo "  ❌ 本日のリサーチなし"
fi
echo ""

echo "【セールスレター制作タスク】"
SL="$BASE/AI活用講義/セールスレター制作"
FOUND=0
for folder in 00_ブレインダンプ 01_Q_絞り込み 02_U_共感 03_E_教育 04_S_刺激 05_T_行動促進 06_競合分析統合 07_価格オファー設計 08_初稿 09_最終完成; do
    if ls "$SL/$folder/${DATE_HYPHEN}*.md" 2>/dev/null | head -1 | grep -q .; then
        FILE=$(ls "$SL/$folder/${DATE_HYPHEN}*.md" | head -1)
        echo "  ✅ $folder：$(basename $FILE)"
        FOUND=1
    fi
done
if [ $FOUND -eq 0 ]; then
    echo "  ❌ 本日のセールスレタータスクなし"
fi
echo ""

echo "【グローバルAI調査】"
GLOBAL="$BASE/AI活用講義/セールスレター制作/06_競合分析統合"
if ls "$GLOBAL/${DATE_HYPHEN}*グローバル*.md" 2>/dev/null | head -1 | grep -q .; then
    echo "  ✅ 本日のグローバル調査あり"
else
    echo "  ❌ 本日のグローバル調査なし"
fi
echo ""

echo "【競合分析（月曜日のみ）】"
WEEKDAY=$(date +%u)
if [ "$WEEKDAY" = "1" ]; then
    COMP="$BASE/競合調査/最新AI講座"
    if ls "$COMP/${DATE_HYPHEN}*.md" 2>/dev/null | head -1 | grep -q .; then
        echo "  ✅ 本日の競合分析あり（月曜日）"
    else
        echo "  ❌ 本日の競合分析なし（月曜日なのに未実行）"
    fi
else
    echo "  ⏭ 本日は月曜日ではないためスキップ"
fi
echo ""

echo "【GitHub同期状況】"
cd "$BASE"
UNPUSHED=$(git log origin/main..HEAD --oneline 2>/dev/null | wc -l)
UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l)
if [ "$UNCOMMITTED" -gt 0 ]; then
    echo "  ⚠️  未コミットのファイルが${UNCOMMITTED}個あります"
    echo "  → git add . && git commit -m '本日分' && git push を実行してください"
else
    echo "  ✅ 全ファイルコミット済み"
fi
echo ""

echo "================================================"
echo "  確認完了"
echo "================================================"
