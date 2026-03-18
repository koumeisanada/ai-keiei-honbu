import google.generativeai as genai
import os
from datetime import datetime

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

COMPANIES = [
    "NVIDIA", "Apple", "Microsoft",
    "Netflix", "Alphabet", "Meta",
    "Amazon", "Tesla", "TSMC"
]

def research_company(company):
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"""
{company}の最新情報を調査してください。

以下の項目を調べて日本語で報告してください：
1. 直近の株価動向・騰落率
2. 最新ニュース・発表事項
3. 決算・業績に関する情報
4. AI・新製品・新サービスの動向
5. アナリスト評価・目標株価
6. 注目すべき重要ポイント

情報は事実のみを記載し、
出典が不明な場合は「〜と報じられている」と明記すること。
"""
    response = model.generate_content(
        prompt,
        tools=[{"google_search": {}}]
    )
    return response.text

def main():
    today = datetime.now().strftime("%Y年%m月%d日")
    date_str = datetime.now().strftime("%Y%m%d")

    save_dir = os.path.expanduser(
        f"~/Desktop/AI経営本部/北の株式投資大学/資料/デイリーリサーチ"
    )
    os.makedirs(save_dir, exist_ok=True)

    output_file = f"{save_dir}/{date_str}_米国株デイリーリサーチ.md"

    content = f"# 米国成長株 デイリーリサーチ\n"
    content += f"**調査日：{today}**\n\n"
    content += "---\n\n"

    for company in COMPANIES:
        print(f"{company}を調査中...")
        result = research_company(company)
        content += f"## {company}\n\n"
        content += result + "\n\n"
        content += "---\n\n"

    with open(output_file, "w") as f:
        f.write(content)

    print(f"✅ 保存完了：{output_file}")
    print(f"✅ {len(COMPANIES)}社の最新情報を収集しました")

if __name__ == "__main__":
    main()
