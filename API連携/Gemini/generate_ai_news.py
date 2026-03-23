from google import genai
from google.genai import types
import os
from datetime import datetime

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

ARCHIVE_DIR = os.path.expanduser(
    "~/Desktop/AI経営本部/集客販売/日次成果物/AI最新情報アーカイブ"
)
DAILY_DIR = os.path.expanduser(
    f"~/Desktop/AI経営本部/集客販売/日次成果物/{datetime.now().strftime('%Y%m%d')}"
)

def load_past_topics():
    past_topics = []
    if os.path.exists(ARCHIVE_DIR):
        files = sorted(os.listdir(ARCHIVE_DIR))[-10:]
        for f in files:
            if f.endswith('.md'):
                with open(os.path.join(ARCHIVE_DIR, f), 'r') as fp:
                    past_topics.append(fp.read()[:500])
    return "\n---\n".join(past_topics) if past_topics else "なし"

def generate_ai_news():
    today = datetime.now().strftime("%Y年%m月%d日")
    past_topics = load_past_topics()

    prompt = f"""
【調査日】{today}

直近のAI業界の最新情報を調査してください。

【重複禁止：以下は過去に既に取り上げたトピックです】
{past_topics[:3000]}

上記と重複しない新しいトピックのみを取り上げてください。

【調査項目】
1. 新しいAIモデルのリリース・アップデート
   （Claude・Gemini・ChatGPT・その他）
2. 米国テクノロジー企業の最新AI戦略
   （NVIDIA・Apple・Microsoft・Meta・Google・Amazon）
3. AI規制・法律の最新動向（日本・EU・米国）
4. 今週登場した話題のAIツール・サービス
5. AIで業績を上げた企業・個人の最新事例
6. 個人ビジネスオーナーが今日から使える具体的な活用方法

【出力形式】

# AI最新情報レポート
## 調査日：{today}

## 今週の重要トピックTOP5
（各トピックに重要度★1〜5を付ける）

## トピック別詳細

### トピック1：[タイトル]
・概要：
・なぜ重要か：
・ビジネスへの影響：
・今日から使える活用方法：
・情報源：

（トピック2〜5も同様）

## 個人ビジネスオーナー向け今週のアクション
（今日から実践できる具体的な3つのアクション）

## 来週注目すべきAIトレンド
（次回の重複防止のため取り上げたトピックを明記）

## 取り上げたトピック一覧（重複防止用）
・[トピック1のキーワード]
・[トピック2のキーワード]
・[トピック3のキーワード]
・[トピック4のキーワード]
・[トピック5のキーワード]

日本語で出力してください。
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        return response.text
    except Exception as e:
        print(f"検索エラー：{e} → 通常モードで再試行")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

def main():
    today = datetime.now().strftime("%Y%m%d")
    today_jp = datetime.now().strftime("%Y年%m月%d日")

    print(f"AI最新情報を収集中... ({today_jp})")

    news = generate_ai_news()

    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    os.makedirs(DAILY_DIR, exist_ok=True)

    archive_file = os.path.join(
        ARCHIVE_DIR,
        f"{today}_AI最新情報.md"
    )
    with open(archive_file, "w") as f:
        f.write(news)
    print(f"✅ アーカイブ保存：{archive_file}")

    daily_file = os.path.join(
        DAILY_DIR,
        "AI最新情報.txt"
    )
    with open(daily_file, "w") as f:
        f.write(news)
    print(f"✅ 日次保存：{daily_file}")

if __name__ == "__main__":
    main()
