from google import genai
from google.genai import types
import os
from datetime import datetime

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SAVE_DIR = os.path.expanduser(
    "~/Desktop/AI経営本部/AI活用講義/セールスレター制作/06_競合分析統合"
)

RESEARCH_THEMES = [
    (
        "CASE01",
        "個人サラリーマン・会社員のAI活用成功事例",
        """
日本・米国・英語圏のセールスレター・LP・SNS・ブログ・ニュース記事から
個人のサラリーマン・会社員がAIを活用して
劇的に状況が変わった成功事例を調査してください。

【調査キーワード】
- "AI活用 サラリーマン 業務効率化 事例"
- "AI tools employee productivity success story"
- "ChatGPT office worker transformation"
- "AI 会社員 残業ゼロ 成功"
- "generative AI employee case study"

【出力形式】各事例について：
■ Before（どんな状態だったか）
■ AI活用方法（何をどう使ったか・具体的なツール名）
■ After（どう変わったか・具体的な数字）
■ セールスレターへの転用フレーズ

最低20事例以上を目標にすること。
"""
    ),
    (
        "CASE02",
        "個人事業主・フリーランスのAI活用成功事例",
        """
個人事業主・フリーランスがAIを活用して
収入・時間・クオリティが劇的に変わった事例を調査してください。

【調査キーワード】
- "AI freelancer income increase case study"
- "個人事業主 AI活用 売上アップ 事例"
- "solopreneur AI automation success"
- "AI フリーランス 生産性 3倍 事例"
- "one person business AI transformation"

【出力形式】各事例について：
■ Before（どんな状態だったか）
■ AI活用方法（何をどう使ったか・具体的なツール名）
■ After（どう変わったか・具体的な数字）
■ セールスレターへの転用フレーズ

最低20事例以上を目標にすること。
"""
    ),
    (
        "CASE03",
        "小規模事業者・中小企業経営者のAI活用成功事例",
        """
小規模事業者・中小企業の経営者がAIを導入して
業績・効率・コストが劇的に変わった事例を調査してください。

【調査キーワード】
- "中小企業 AI導入 効果 事例"
- "small business AI implementation success"
- "AI 経営者 コスト削減 事例"
- "SMB AI transformation case study"
- "AI 売上向上 小規模 事例"

【出力形式】各事例について：
■ Before（どんな状態だったか）
■ AI活用方法（何をどう使ったか・具体的なツール名）
■ After（どう変わったか・具体的な数字）
■ セールスレターへの転用フレーズ

最低20事例以上を目標にすること。
"""
    ),
    (
        "CASE04",
        "コンテンツ制作・マーケティングのAI活用成功事例",
        """
ブログ・SNS・動画・メルマガ・広告など
コンテンツ制作とマーケティングでAIを活用して
成果が劇的に変わった事例を調査してください。

【調査キーワード】
- "AI content creation ROI case study"
- "AI マーケティング 成果 事例"
- "ChatGPT content marketing success"
- "AI SNS 運用 フォロワー増加 事例"
- "generative AI marketing transformation"

【出力形式】各事例について：
■ Before（どんな状態だったか）
■ AI活用方法（何をどう使ったか・具体的なツール名）
■ After（どう変わったか・具体的な数字）
■ セールスレターへの転用フレーズ

最低20事例以上を目標にすること。
"""
    ),
    (
        "CASE05",
        "業務自動化・時間削減のAI活用成功事例",
        """
繰り返し作業・定型業務をAIで自動化して
時間が劇的に増えた事例を調査してください。

【調査キーワード】
- "AI workflow automation time saved"
- "AI 業務自動化 時間削減 事例"
- "RPA AI automation success story"
- "AI pipeline automation small business"
- "AI 定型業務 自動化 効果"

【出力形式】各事例について：
■ Before（どんな状態だったか・何時間かかっていたか）
■ AI活用方法（何をどう自動化したか・具体的なツール名）
■ After（何時間削減できたか・具体的な数字）
■ セールスレターへの転用フレーズ

最低20事例以上を目標にすること。
"""
    ),
    (
        "CASE06",
        "40代・50代・アラフィフのAI活用成功事例",
        """
特に40代・50代・ITに不慣れな世代が
AIを活用して劇的に変わった事例を調査してください。

【調査キーワード】
- "40代 AI活用 成功 事例"
- "middle aged AI technology adoption success"
- "50代 デジタル変革 成功 事例"
- "non-technical person AI success story"
- "アラフィフ AI 仕事 変わった"

【出力形式】各事例について：
■ Before（どんな状態だったか・IT苦手意識など）
■ AI活用方法（何をどう使ったか・具体的なツール名）
■ After（どう変わったか・具体的な数字）
■ セールスレターへの転用フレーズ

最低15事例以上を目標にすること。
"""
    ),
    (
        "CASE07",
        "AI活用による収入・副業・ビジネス成功事例",
        """
AIを活用して副業・新規ビジネスで
収入が劇的に増えた事例を調査してください。

【調査キーワード】
- "AI side hustle income success"
- "AI 副業 収入 事例"
- "AI business launch success story"
- "making money with AI case study"
- "AI 起業 成功 事例"

【出力形式】各事例について：
■ Before（どんな状態だったか・収入など）
■ AI活用方法（何をどう使ったか・具体的なツール名）
■ After（どう変わったか・具体的な収入数字）
■ セールスレターへの転用フレーズ

最低20事例以上を目標にすること。
"""
    ),
]

def research_cases(case_id, case_name, prompt_detail):
    today = datetime.now().strftime("%Y年%m月%d日 %H:%M")

    prompt = f"""
【調査日】{today}
【調査テーマ】{case_name}

{prompt_detail}

【重要な調査ルール】
・直近2年以内の最新情報を優先する
・日本国内と英語圏（米国・英国・豪州）両方を調査する
・セールスレター・LP・ブログ・ニュース・SNSから実例を収集する
・具体的な数字（時間・収入・コスト削減率等）を必ず含める
・ツール名（Claude・ChatGPT・Gemini・Midjourney等）を具体的に記載する
・URLや情報源を可能な限り明記する

【真田孔明のAI講座への転用視点】
各事例の最後に必ず以下を記載すること：
→ セールスレターのどのパート（Q/U/E/S/T）に使えるか
→ 具体的な転用フレーズ案
→ ターゲット（サラリーマン・個人事業主・経営者）への刺さり度（★1〜5）

【出力形式】
## {case_id}：{case_name}

### 事例一覧

#### 事例[番号]：[タイトル]
■ Before：
■ AI活用方法：
■ After：
■ 転用フレーズ：
■ 使えるパート：
■ 刺さり度：★★★★★
"""

    print(f"\n{case_id}：{case_name} を調査中...")

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
        print(f"エラー：{e}")
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e2:
            return f"調査失敗：{e2}"

def main():
    os.makedirs(SAVE_DIR, exist_ok=True)
    cases_dir = os.path.join(SAVE_DIR, "AI活用成功事例集")
    os.makedirs(cases_dir, exist_ok=True)

    all_results = "# AI活用成功事例集 完全版\n"
    all_results += f"## 調査日：{datetime.now().strftime('%Y年%m月%d日')}\n"
    all_results += "## 目的：セールスレターのS（刺激）・U（共感）パートへの転用\n\n"
    all_results += "---\n\n"

    for case_id, case_name, prompt_detail in RESEARCH_THEMES:
        result = research_cases(case_id, case_name, prompt_detail)

        individual_file = os.path.join(
            cases_dir,
            f"{case_id}_{case_name}.md"
        )
        with open(individual_file, "w") as f:
            f.write(f"# {case_id}：{case_name}\n\n")
            f.write(result)

        all_results += f"\n\n---\n\n{result}"
        print(f"✅ {case_id} 完了・保存：{individual_file}")

    all_file = os.path.join(cases_dir, "00_AI活用成功事例_全テーマ統合.md")
    with open(all_file, "w") as f:
        f.write(all_results)

    print(f"\n✅ 全7テーマの成功事例調査完了")
    print(f"✅ 統合ファイル：{all_file}")

    import subprocess
    subprocess.run([
        "bash", "-c",
        "cd ~/Desktop/AI経営本部 && "
        "git add AI活用講義/セールスレター制作/06_競合分析統合/ && "
        "git commit -m 'AI活用成功事例集 全7テーマ調査完了' && "
        "git push origin salesletter-development"
    ])

    print("✅ GitHubプッシュ完了")
    print("確認URL：https://github.com/koumeisanada/ai-keiei-honbu/blob/salesletter-development/AI活用講義/セールスレター制作/06_競合分析統合/AI活用成功事例集/00_AI活用成功事例_全テーマ統合.md")

if __name__ == "__main__":
    main()
