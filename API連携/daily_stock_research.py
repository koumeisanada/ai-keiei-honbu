import google.generativeai as genai
import os
from datetime import datetime

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

COMPANIES = [
    "NVIDIA", "Apple", "Microsoft",
    "Netflix", "Alphabet", "Meta",
    "Amazon", "Tesla", "TSMC"
]

SOURCES = """
調査対象メディア・情報源：
- The Verge / Wired / TechCrunch / Ars Technica
- Bloomberg Technology / Reuters Technology
- CNBC Tech / Wall Street Journal Tech
- MIT Technology Review
- The Information
- 各社公式プレスリリース・投資家向け資料
- CEO・幹部のX（Twitter）・インタビュー発言
"""

def research_company(company):
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"""{company}の「5年〜10年先の成長性」に関わる最新情報を米国の主要テクノロジーメディアから調査してください。

{SOURCES}

【調査項目】
1. 最新プロジェクト・研究開発の動向
   - 発表済みの新技術・新製品・新サービス
   - 開発中と報じられているもの
   - 特許申請・取得情報

2. 戦略的提携・M&A・投資動向
   - 新たなパートナーシップ
   - 買収・出資情報
   - 新市場への参入

3. AI・次世代技術への取り組み
   - AI開発の最新状況
   - 次世代製品のロードマップ
   - 競合との差別化要素

4. CEO・幹部の発言・ビジョン
   - 将来に関する重要発言
   - 投資家向け説明会での発言
   - インタビューでの方向性

5. 業界トレンドとの関係性
   - 市場全体の変化と{company}の位置づけ
   - 5〜10年後に影響する構造的変化

【重要ルール】
・株価・決算数字は不要
・事実情報には情報源を明記する
・噂・未確認情報は「〜と報じられている」「〜との情報がある」と明記
・長期成長に関係しない短期的なニュースは除外する
・日本語で報告すること"""

    try:
        response = model.generate_content(
            prompt,
            tools="google_search_retrieval"
        )
    except Exception:
        response = model.generate_content(prompt)
    return response.text

def main():
    today = datetime.now().strftime("%Y年%m月%d日")
    date_str = datetime.now().strftime("%Y%m%d")

    save_dir = os.path.expanduser(
        "~/Desktop/AI経営本部/北の株式投資大学/資料/デイリーリサーチ"
    )
    os.makedirs(save_dir, exist_ok=True)

    output_file = f"{save_dir}/{date_str}_米国成長株リサーチ.md"

    content = "# 米国成長株 最新動向リサーチ\n"
    content += f"**調査日：{today}**\n"
    content += "**テーマ：5〜10年先の成長性に関わる最新プロジェクト・発表・動向**\n\n"
    content += "---\n\n"

    for company in COMPANIES:
        print(f"{company}を調査中...")
        result = research_company(company)
        content += f"## {company}\n\n"
        content += result + "\n\n"
        content += "---\n\n"

    content += "## 本日の注目トレンド総括\n\n"

    model = genai.GenerativeModel('gemini-2.5-flash')
    summary_prompt = """以下の9社（NVIDIA・Apple・Microsoft・Netflix・Alphabet・Meta・Amazon・Tesla・TSMC）の本日の調査結果を踏まえて、5〜10年先の米国テクノロジー業界全体のトレンドとして特に注目すべきポイントを3〜5つ日本語でまとめてください。長期投資家として「これは重要だ」と感じる視点で総括してください。"""

    try:
        summary = model.generate_content(
            summary_prompt,
            tools="google_search_retrieval"
        )
    except Exception:
        summary = model.generate_content(summary_prompt)

    content += summary.text + "\n\n"

    with open(output_file, "w") as f:
        f.write(content)

    print(f"✅ 保存完了：{output_file}")
    print(f"✅ 対象9社の最新動向リサーチ完了")
    print(f"✅ 5〜10年先成長性トレンド総括も追加済み")

if __name__ == "__main__":
    main()
