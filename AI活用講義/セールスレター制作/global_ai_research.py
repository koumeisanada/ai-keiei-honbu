from google import genai
from google.genai import types
import os
import glob
from datetime import datetime, date

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

BASE_DIR = os.path.expanduser(
    "~/Desktop/AI経営本部/AI活用講義/セールスレター制作/06_競合分析統合"
)

RESEARCH_SCHEDULE = {
    "2026-03-19": {
        "title": "米国AI講座_価格帯とターゲット調査",
        "prompt": """
英語圏（主に米国・英国・オーストラリア）で個人向けに販売されている
AI活用・AIエージェント・AI自動化講座を調査してください。

【調査対象】
・サラリーマン・個人事業主・小規模事業者向け
・月額50〜300ドル程度のサブスク型
・または一括1,000〜5,000ドル程度の講座

【調査項目】
1. 講座名・提供者名・URL
2. 価格設定と課金モデル
3. メインターゲット（誰に向けて売っているか）
4. 受講者数・売上規模（公開情報のみ）
5. 最も売れている講座の特徴

【調査対象キーワード】
- "AI automation course for solopreneurs"
- "AI agent training for small business"
- "AI workflow automation membership"
- "ChatGPT course for entrepreneurs"
- "AI business automation coaching"

日本語で報告してください。
"""
    },
    "2026-03-20": {
        "title": "米国AI講座_セールスレター表現調査",
        "prompt": """
英語圏で最も売れているAI活用講座のセールスレター・LP（ランディングページ）を調査してください。

【調査項目】
1. ヘッドラインの表現パターン（最初の一文でどう掴むか）
2. 痛み・問題提起の言葉（どんな言葉で共感を取るか）
3. ベネフィットの伝え方（何が手に入ると言っているか）
4. 社会的証明の見せ方（実績・受講者の声の使い方）
5. 価格の正当化方法（なぜこの値段なのかの説明）
6. 緊急性・希少性の作り方
7. クロージングの言葉

【注目すべきクリエイター・講座】
- Sam Ovens（Skool）
- Dan Martell（SaaS Academy）
- Iman Gadzhi（AI自動化系）
- Nicholas Kusmich（Facebook広告×AI）
- その他トップセラー

日本語で報告・分析してください。
真田孔明の講座に転用できる表現は特に詳しく分析すること。
"""
    },
    "2026-03-21": {
        "title": "米国AI講座_カリキュラム内容調査",
        "prompt": """
英語圏で最も人気のあるAI活用講座のカリキュラム内容を調査してください。

【調査項目】
1. 年間・月次のカリキュラム構成
2. 最も人気の高い講義テーマTop10
3. 受講者が最も価値を感じているコンテンツ
4. 競合が教えていないが需要が高いテーマ
5. AIエージェント・AI自動化の具体的な教え方
6. ツール別の人気度（Claude・ChatGPT・Gemini・Make・Zapier等）

【注目すべきカリキュラム】
- AI Business Automation（Make・Zapier活用）
- AI Agent Building（n8n・AutoGPT等）
- AI Content Creation System
- AI Lead Generation
- AI Customer Service Automation

【真田孔明の講座への転用ポイント】
日本市場向けにローカライズできる内容を特に分析すること。
年間12回の講義設計のヒントになる情報を抽出すること。

日本語で報告してください。
"""
    },
    "2026-03-22": {
        "title": "米国AI講座_プロジェクト名・ブランディング調査",
        "prompt": """
英語圏で成功しているAI講座・コミュニティの
プロジェクト名・ブランディング戦略を調査してください。

【調査項目】
1. 成功している講座名の命名パターン
2. どんな言葉・コンセプトが40代以上に刺さるか
3. コミュニティ名の特徴（所属感・仲間意識を高める名前）
4. ロゴ・ビジュアルアイデンティティの傾向
5. タグライン（キャッチコピー）の表現パターン

【真田孔明の講座名候補への転用】
以下の方向性で日本語名・英語名を各5案提案すること：
- AI組織・経営系
- 自由・ライフスタイル系
- 設計図・OS系
- アラフィフ・世代系

日本語で報告してください。
"""
    },
}

def load_past_research():
    past = []
    for f in glob.glob(f"{BASE_DIR}/*_グローバル調査*.md"):
        with open(f, "r") as fp:
            past.append(fp.read()[:1000])
    return "\n\n---\n\n".join(past[:5]) if past else ""

def run_research():
    today_str = date.today().strftime("%Y-%m-%d")
    today_display = date.today().strftime("%Y年%m月%d日")

    if today_str not in RESEARCH_SCHEDULE:
        print(f"本日（{today_display}）のグローバル調査スケジュールはありません")
        return

    task = RESEARCH_SCHEDULE[today_str]
    past = load_past_research()

    full_prompt = f"""
【調査日】{today_display}
【過去の調査データ（重複禁止）】
{past if past else "初回調査"}

{task["prompt"]}

【重要】
・直近1ヶ月以内の最新情報を優先すること
・情報源（URL・サイト名）を必ず明記すること
・真田孔明の講座設計に直接使えるアイデアを太字で強調すること
・WHY（なぜこれが重要か）を各項目に付けること
"""

    print(f"グローバル調査実行中：{task['title']}")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
    except Exception:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )

    os.makedirs(BASE_DIR, exist_ok=True)
    output_file = os.path.join(
        BASE_DIR,
        f"{today_str}_グローバル調査_{task['title']}.md"
    )

    content = f"# グローバル調査：{task['title']}\n"
    content += f"**調査日：{today_display}**\n\n"
    content += "---\n\n"
    content += response.text

    with open(output_file, "w") as f:
        f.write(content)

    print(f"✅ 保存完了：{output_file}")

if __name__ == "__main__":
    run_research()
