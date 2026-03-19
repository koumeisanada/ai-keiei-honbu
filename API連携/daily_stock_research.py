from google import genai
from google.genai import types
import os
import glob
from datetime import datetime

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

COMPANIES = [
    "NVIDIA", "Apple", "Microsoft",
    "Netflix", "Alphabet", "Meta",
    "Amazon", "Tesla", "TSMC"
]

def load_past_research(company, days=7):
    save_dir = os.path.expanduser(
        "~/Desktop/AI経営本部/北の株式投資大学/資料/デイリーリサーチ"
    )
    files = sorted(glob.glob(f"{save_dir}/*_米国成長株リサーチ.md"), reverse=True)
    past_content = []
    for f in files[:days]:
        with open(f, "r") as fp:
            content = fp.read()
            start = content.find(f"## {company}")
            if start != -1:
                end = content.find("## ", start + 1)
                section = content[start:end] if end != -1 else content[start:]
                past_content.append(section[:2000])
    return "\n\n---過去の調査---\n\n".join(past_content) if past_content else ""

def research_company(company):
    past = load_past_research(company)
    past_section = f"""
【過去7日間の調査済み情報（重複禁止）】
{past}
上記の内容と重複する情報は報告しないでください。
新しい情報・新たな進展のみを報告してください。
過去と同じ内容の場合は「本日の新規情報なし」と記載してください。
""" if past else "（初回調査のため過去データなし）"

    today_str = datetime.now().strftime("%Y年%m月%d日")
    prompt = f"""【最重要：調査期間の制限】
調査対象期間：直近7日以内に発表・報道された情報のみ
それ以前の情報は一切含めないこと
情報には必ず「いつ報道されたか」の日付を明記すること
日付が不明な情報は掲載しないこと
2024年以前の情報は絶対に含めないこと

{company}の「5年〜10年先の成長性」に関わる【本日の新着情報のみ】を
米国の主要テクノロジーメディアから調査してください。

調査期間：{today_str}から遡って7日以内の情報のみ
それ以外の情報は「情報なし」と記載すること

{past_section}

【調査項目】
1. 最新プロジェクト・研究開発の新着動向
2. 戦略的提携・M&A・投資の新着情報
3. AI・次世代技術の新着発表
4. CEO・幹部の新着発言・ビジョン
5. 業界トレンドの新着変化

【重要ルール】
・株価・決算数字は不要
・過去調査済みの情報は絶対に繰り返さない
・事実情報には情報源を明記する
・噂・未確認情報は「〜と報じられている」と明記
・新情報がない場合は「本日の新規情報なし」と明記
・日本語で報告すること"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
    )
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
    content += "**テーマ：5〜10年先の成長性に関わる新着情報のみ（重複除外）**\n\n"
    content += "---\n\n"

    for company in COMPANIES:
        print(f"{company}を調査中...")
        result = research_company(company)
        content += f"## {company}\n\n"
        content += result + "\n\n"
        content += "---\n\n"

    content += "## 本日の注目トレンド総括\n\n"

    summary_prompt = """9社（NVIDIA・Apple・Microsoft・Netflix・Alphabet・Meta・Amazon・Tesla・TSMC）の
本日の新着調査結果を踏まえて、
5〜10年先の米国テクノロジー業界で特に注目すべき新着ポイントを
3〜5つ日本語でまとめてください。
長期投資家の視点で総括してください。"""

    summary = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=summary_prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
    )
    content += summary.text + "\n\n"

    with open(output_file, "w") as f:
        f.write(content)

    print(f"✅ 保存完了：{output_file}")
    print(f"✅ 対象9社の新着情報リサーチ完了")
    print(f"✅ 過去7日間の重複情報を自動除外済み")

if __name__ == "__main__":
    main()
