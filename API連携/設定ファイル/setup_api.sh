#!/bin/bash
echo "=== AI経営本部 API連携セットアップ ==="
echo "Gemini APIキーを入力してください："
read GEMINI_KEY
echo "export GEMINI_API_KEY=$GEMINI_KEY" >> ~/.zshrc
echo "OpenAI APIキーを入力してください："
read OPENAI_KEY
echo "export OPENAI_API_KEY=$OPENAI_KEY" >> ~/.zshrc
source ~/.zshrc
echo "=== APIキーの設定が完了しました ==="
