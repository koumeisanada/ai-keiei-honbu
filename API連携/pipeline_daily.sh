#!/bin/bash
echo "================================================"
echo "  真田孔明AI経営本部 デイリーパイプライン"
echo "================================================"
echo ""
echo "今日のメルマガのテーマを入力してください："
echo "（例：物価上昇で苦しむ40代サラリーマンの逆転戦略）"
read THEME
echo ""

echo "【米国株デイリーリサーチ実行中...】"
python3 ~/Desktop/AI経営本部/API連携/daily_stock_research.py
echo "✅ 米国株リサーチ完了"
echo ""

DATE=$(date +%Y%m%d)
mkdir -p ~/Desktop/AI経営本部/集客販売/日次成果物/$DATE

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
