from google import genai
from google.genai import types
import os
import sys
from datetime import datetime

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

COMPANIES = {
    "NVIDIA": {
        "competitors": ["AMD", "Intel", "Qualcomm", "Broadcom"],
        "group": "AI半導体",
        "special_notes": "TSMCとの製造依存関係・Blackwellロードマップ"
    },
    "Apple": {
        "competitors": ["Samsung", "Google Pixel", "Huawei"],
        "group": "コンシューマー",
        "special_notes": "Apple Intelligence展開・サービス収益化"
    },
    "Microsoft": {
        "competitors": ["Google", "Amazon AWS", "Oracle"],
        "group": "プラットフォーム",
        "special_notes": "OpenAI投資・Copilot展開・Azure成長"
    },
    "Netflix": {
        "competitors": ["Disney+", "Amazon Prime", "YouTube"],
        "group": "コンシューマー",
        "special_notes": "AI活用コンテンツ制作・広告収益化"
    },
    "Alphabet": {
        "competitors": ["Microsoft", "Amazon", "Meta"],
        "group": "プラットフォーム",
        "special_notes": "Gemini・Waymo・検索広告のAI統合"
    },
    "Meta": {
        "competitors": ["TikTok", "Apple", "Google"],
        "group": "プラットフォーム",
        "special_notes": "Llama・AR/VR・広告AI最適化"
    },
    "Amazon": {
        "competitors": ["Microsoft Azure", "Google Cloud", "Shopify"],
        "group": "プラットフォーム",
        "special_notes": "AWS・Bedrock・物流AI自動化"
    },
    "Tesla": {
        "competitors": ["BYD", "Waymo", "Toyota"],
        "group": "コンシューマー",
        "special_notes": "FSD・Robotaxi・Optimus人型ロボット"
    },
    "TSMC": {
        "competitors": ["Samsung Foundry", "Intel Foundry", "SMIC"],
        "group": "製造インフラ",
        "special_notes": "台湾地政学リスク・2nm技術・米国工場"
    }
}

def enhance_analysis(company):
    info = COMPANIES.get(company, {})
    competitors = "・".join(info.get("competitors", []))
    special_notes = info.get("special_notes", "")
    today = datetime.now().strftime("%Y年%m月%d日")

    prompt = f"""
{company}の企業考察資料を強化するための
補完情報を調査・生成してください。

調査日：{today}
対象企業：{company}
競合比較対象：{competitors}
特記事項：{special_notes}

【出力1：競合比較分析】
{company}と{competitors}を以下の軸で比較してください。

1. AI技術力・開発ロードマップの比較
2. 市場シェアと5年後の予測
3. 収益性・投資効率の比較
4. 独自の競争優位性（モート）の強度比較
5. {company}が競合に対して有利な点・不利な点

【出力2：リスク要因の深堀り】
{company}の長期投資家が必ず把握すべきリスクを分析してください。

1. 地政学リスク
   - 米中関係の影響
   - TSMCへの依存度（該当する場合）
   - 輸出規制・制裁の影響

2. 規制リスク
   - 米国・EU・中国の規制動向
   - AI規制の影響

3. 競合リスク
   - 既存競合の追い上げ
   - 中国企業の脅威
   - オープンソースの影響

4. 技術リスク
   - 現在の優位性の持続可能性
   - 次世代技術への対応

5. 財務リスク
   - AI投資の収益化タイムライン
   - 過剰投資リスク

【重要ルール】
・直近3ヶ月以内の最新情報を優先すること
・情報源を明記すること
・事実と考察を明確に区別すること
・株価・投資推奨は含めないこと
・日本語で出力すること
・5〜10年の長期視点で分析すること
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
    except Exception:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

    return response.text

def main():
    today_str = datetime.now().strftime("%Y%m%d")
    save_dir = os.path.expanduser(
        "~/Desktop/AI経営本部/北の株式投資大学/資料/競合比較・リスク分析"
    )
    os.makedirs(save_dir, exist_ok=True)

    if len(sys.argv) > 1:
        companies = [sys.argv[1]]
    else:
        companies = list(COMPANIES.keys())

    for company in companies:
        print(f"{company}の補強分析を実行中...")
        result = enhance_analysis(company)

        output_file = os.path.join(
            save_dir,
            f"{today_str}_{company}_競合比較・リスク分析.md"
        )

        content = f"# {company} 競合比較・リスク分析\n"
        content += f"**分析日：{datetime.now().strftime('%Y年%m月%d日')}**\n"
        content += f"**競合対象：{' '.join(COMPANIES[company]['competitors'])}**\n\n"
        content += "---\n\n"
        content += result

        with open(output_file, "w") as f:
            f.write(content)

        print(f"✅ 保存完了：{output_file}")

    print(f"\n✅ 全{len(companies)}社の補強分析完了")
    print(f"保存先：{save_dir}")

if __name__ == "__main__":
    main()
