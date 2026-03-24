#!/bin/bash
# 環境変数の読み込み（LaunchAgent経由では.zshrcが読み込まれないため）
source ~/.zshrc 2>/dev/null
export GEMINI_API_KEY=$(grep GEMINI_API_KEY ~/.zshrc | cut -d'"' -f2)
export OPENAI_API_KEY=$(grep OPENAI_API_KEY ~/.zshrc | cut -d'"' -f2)
export ANTHROPIC_API_KEY=$(grep ANTHROPIC_API_KEY ~/.zshrc | cut -d'"' -f2)

# ログファイル設定（cron実行時の確認用）
LOGDIR=~/Desktop/AI経営本部/集客販売/日次成果物
DATE=$(date +%Y%m%d)
LOGFILE="$LOGDIR/$DATE/pipeline.log"
mkdir -p "$LOGDIR/$DATE"

# 全出力をログにも記録
exec > >(tee -a "$LOGFILE") 2>&1

echo "================================================"
echo "  真田孔明AI経営本部 デイリーパイプライン"
echo "  実行時刻：$(date '+%Y-%m-%d %H:%M:%S')"
echo "================================================"
echo ""

# --- テーマ取得 ---
# 引数があればそれを使用、なければテーマファイル、なければデフォルト
THEME_FILE=~/Desktop/AI経営本部/API連携/設定ファイル/tomorrow_theme.txt
DEFAULT_THEME="今日の最新ニュースから40代サラリーマンに刺さるテーマを選んで"

if [ -n "$1" ]; then
    # 手動実行時：引数からテーマ取得
    THEME="$1"
    echo "テーマ（引数指定）：$THEME"
elif [ -t 0 ]; then
    # 対話モード：手動入力を受付
    echo "今日のメルマガのテーマを入力してください："
    echo "（例：物価上昇で苦しむ40代サラリーマンの逆転戦略）"
    echo "（空Enterでテーマファイルを使用）"
    read THEME
    if [ -z "$THEME" ]; then
        if [ -s "$THEME_FILE" ]; then
            THEME=$(cat "$THEME_FILE")
        else
            THEME="$DEFAULT_THEME"
        fi
        echo "テーマ（ファイル/デフォルト）：$THEME"
    fi
else
    # cron等の非対話モード：テーマファイル→デフォルトの順
    if [ -s "$THEME_FILE" ]; then
        THEME=$(cat "$THEME_FILE")
        echo "テーマ（ファイルから取得）：$THEME"
    else
        THEME="$DEFAULT_THEME"
        echo "テーマ（デフォルト）：$THEME"
    fi
fi
echo ""

# テーマ使用後、ファイルをデフォルトにリセット
echo "$DEFAULT_THEME" > "$THEME_FILE"

echo "【前日の品質チェック結果を反映中...】"
python3 ~/Desktop/AI経営本部/API連携/Gemini/apply_feedback.py
echo "✅ 前日のフィードバック反映完了"
echo ""

echo "【Step1】メルマガを生成中...（Gemini使用）"
for i in 1 2 3; do
  python3 ~/Desktop/AI経営本部/API連携/Gemini/generate_merumaga.py "$THEME" > ~/Desktop/AI経営本部/集客販売/日次成果物/$DATE/メルマガ.txt
  if [ -s ~/Desktop/AI経営本部/集客販売/日次成果物/$DATE/メルマガ.txt ]; then
    break
  fi
  echo "⚠️  Gemini APIエラー。${i}回目リトライ中...（5秒後）"
  sleep 5
done
if [ ! -s ~/Desktop/AI経営本部/集客販売/日次成果物/$DATE/メルマガ.txt ]; then
  echo "❌ メルマガ生成に失敗しました。Gemini APIの状態を確認してください。"
  exit 1
fi
echo "✅ メルマガ完了"
echo ""

echo "AI最新情報を収集中..."
python3 ~/Desktop/AI経営本部/API連携/Gemini/generate_ai_news.py
echo "✅ AI最新情報収集完了"
echo ""

echo "【Step2】LINE4日分を生成中...（Gemini使用）"
python3 ~/Desktop/AI経営本部/API連携/Gemini/generate_line_4days.py "$(cat ~/Desktop/AI経営本部/集客販売/日次成果物/$DATE/メルマガ.txt)" > ~/Desktop/AI経営本部/集客販売/日次成果物/$DATE/LINE4日分.txt
echo "✅ LINE4日分完了"
echo ""

echo "【Step3】リール動画原稿を生成中...（Gemini使用）"
python3 ~/Desktop/AI経営本部/API連携/Gemini/generate_reel.py "$(cat ~/Desktop/AI経営本部/集客販売/日次成果物/$DATE/メルマガ.txt)" > ~/Desktop/AI経営本部/集客販売/日次成果物/$DATE/リール動画原稿.txt
echo "✅ リール動画原稿完了"
echo ""

echo "【Step4】ストーリー画像プロンプトを生成中..."
claude --print "以下のメルマガのテーマに合わせて、ゼータスタイルのInstagramストーリー画像プロンプトを1つ生成してください：$(cat ~/Desktop/AI経営本部/集客販売/日次成果物/$DATE/メルマガ.txt | head -c 500)" > ~/Desktop/AI経営本部/集客販売/日次成果物/$DATE/ストーリー画像プロンプト.txt
echo "✅ ストーリー画像プロンプト完了"
echo ""

echo "【競合分析実行中...（週1回）】"
DAY_OF_WEEK=$(date +%u)
if [ "$DAY_OF_WEEK" = "1" ]; then
    python3 ~/Desktop/AI経営本部/競合調査/ai_competitor_research.py
    echo "✅ 競合分析完了"
else
    echo "（競合分析は毎週月曜日に自動実行）"
fi
echo ""

echo "【セールスレター制作 本日のタスク実行中...】"
echo "午前・午後の2回実行します"
python3 ~/Desktop/AI経営本部/AI活用講義/セールスレター制作/daily_salesletter.py
echo "✅ セールスレタータスク完了"
echo ""

echo "【グローバルAI講座調査実行中...】"
python3 ~/Desktop/AI経営本部/AI活用講義/セールスレター制作/global_ai_research.py
echo "✅ グローバル調査完了"
echo ""

echo "ケイタ式 eBayリサーチ実行中..."
python3 ~/Desktop/AI経営本部/物販ビジネス/ケイタ式/自動化スクリプト/ebay_japan_research.py
echo "✅ ケイタ式 eBayリサーチ完了"
echo ""

echo "【米国企業リサーチ実行中...（Gemini使用）】"
echo "米国企業リサーチ開始..."
python3 ~/Desktop/AI経営本部/API連携/daily_stock_research.py
echo "✅ 米国企業リサーチ完了"
echo ""

echo "【Step5】品質チェック中...（Claude使用）"
claude --print "以下のメルマガを品質チェックして100点満点でスコアリングしてください：$(cat ~/Desktop/AI経営本部/集客販売/日次成果物/$DATE/メルマガ.txt)" > ~/Desktop/AI経営本部/集客販売/日次成果物/$DATE/品質チェック結果.txt
echo "✅ 品質チェック完了"
echo ""

echo "================================================"
echo "  本日の成果物が完成しました！"
echo "================================================"
echo ""
echo "保存先：Desktop/AI経営本部/集客販売/日次成果物/$DATE/"
echo ""
echo "✅ メルマガ.txt（約4,000文字）"
echo "✅ LINE4日分.txt（各900〜1000文字）"
echo "✅ リール動画原稿.txt（200〜250文字）"
echo "✅ ストーリー画像プロンプト.txt"
echo "✅ 品質チェック結果.txt"
echo ""
echo "次のステップ："
echo "1. ストーリー画像プロンプト.txtを開く"
echo "2. Gemini（ナノバナナプロ）に貼り付けて画像生成"
echo "3. 各媒体に投稿！"
echo "================================================"

echo ""
echo "【本日のアウトプット確認レポート】"
bash ~/Desktop/AI経営本部/API連携/check_progress.sh
