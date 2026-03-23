from google import genai
from google.genai import types
import os
import glob
from datetime import datetime

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def load_past_research(days=14):
    save_dir = os.path.expanduser(
        "~/Desktop/AI経営本部/競合調査/最新AI講座"
    )
    files = sorted(glob.glob(f"{save_dir}/*_競合分析.md"), reverse=True)
    past_content = []
    for f in files[:days]:
        with open(f, "r") as fp:
            past_content.append(fp.read()[:3000])
    return "\n\n---過去調査---\n\n".join(past_content) if past_content else ""

def research_competitors():
    past = load_past_research()
    past_section = f"""
【過去14日間の調査済み情報（重複禁止）】
{past}
上記と重複する情報は報告しないでください。
新しい情報・新たな動向のみを報告してください。
""" if past else "（初回調査のため過去データなし）"

    today_str = datetime.now().strftime("%Y年%m月%d日")

    prompt = f"""
【最重要：調査期間の制限】
調査対象期間：直近14日以内に発表・掲載された情報のみ
それ以前の情報は一切含めないこと
情報には必ず「いつ掲載されたか」の日付を明記すること
日付が不明な情報は掲載しないこと

調査日：{today_str}

日本国内の「AI活用・AI副業・AI自動化・AI経営」を教える
情報発信者・コミュニティ・オンラインスクールの競合分析を行ってください。

{past_section}

【調査対象カテゴリー】
1. AI副業・AI収益化系（月額サブスク・高額塾）
2. AI自動化・業務効率化系（経営者・管理職向け）
3. AI×マーケティング系（集客・販売自動化）
4. AI×投資・資産形成系
5. 中高年・アラフィフ向けAI活用系

【各競合について調査する項目】
1. 発信者名・コミュニティ名・URL
2. セールスメッセージの核心（どんな言葉で売っているか）
3. 商品・サービスの内容と価格帯
4. ターゲット層（誰に向けて売っているか）
5. 集客方法（Instagram・YouTube・メルマガ等）
6. セールスレター・LP・ブログの訴求ポイント
7. 強み・差別化ポイント
8. 弱み・課題・批判的な声

【真田孔明の最新AI講座との比較分析】
真田孔明の最新AI講座の差別化ポイントを以下の視点で分析：
・他の競合にない独自の強み
・価格競争力
・ターゲットの重複・空白地帯
・今すぐ使えるセールスメッセージのヒント

【調査対象メディア】
・Google検索（セールスレター・LP）
・note・ブログ
・Instagram・YouTube
・X（Twitter）
・各種メルマガ

【重要ルール】
・過去調査済みの情報は繰り返さない
・新情報がない場合は「本日の新規情報なし」と明記
・日本語で報告すること
・具体的な固有名詞・URL・価格を可能な限り明記すること
"""

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
        "~/Desktop/AI経営本部/競合調査/最新AI講座"
    )
    os.makedirs(save_dir, exist_ok=True)

    output_file = f"{save_dir}/{date_str}_競合分析.md"

    print("AI講座競合分析を開始します...")
    result = research_competitors()

    content = "# 最新AI講座 競合分析レポート\n"
    content += f"**調査日：{today}**\n"
    content += "**対象：日本国内AI活用・AI副業・AI自動化系競合**\n\n"
    content += "---\n\n"
    content += result
    content += "\n\n---\n\n"
    content += "## 真田孔明 最新AI講座の差別化戦略メモ\n\n"
    content += "※上記分析を踏まえて、次回セールスレター作成時に活用すること\n"

    with open(output_file, "w") as f:
        f.write(content)

    print(f"✅ 保存完了：{output_file}")
    print(f"✅ 競合分析レポート完成")

if __name__ == "__main__":
    main()
