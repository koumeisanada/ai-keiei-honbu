from google import genai
from google.genai import types
import os
from datetime import datetime

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SAVE_DIR = os.path.expanduser(
    "~/Desktop/AI経営本部/AI活用講義/セールスレター制作/06_競合分析統合/日本AI講座分析"
)

TARGETS = [
    (
        "SCHOOL01",
        "機械学習 longterm.kikagaku.ai",
        "https://longterm.kikagaku.ai/2#kikagakuai",
        "kikagaku AI longterm 機械学習 講座"
    ),
    (
        "SCHOOL02",
        "Shift AI",
        "https://shift-ai.co.jp/service-lp/",
        "Shift AI 講座 カリキュラム 料金"
    ),
    (
        "SCHOOL03",
        "Life Shift Lab",
        "https://lifeshiftlab.jp/ai",
        "Life Shift Lab AI 講座 内容"
    ),
    (
        "SCHOOL04",
        "ホリエモンAI学校",
        "https://horiemon.ai/",
        "ホリエモン AI学校 講座 カリキュラム 料金"
    ),
]

def analyze_school(school_id, school_name, url, search_query):
    today = datetime.now().strftime("%Y年%m月%d日")

    prompt = f"""
【調査日】{today}
【調査対象】{school_name}
【URL】{url}
【検索キーワード】{search_query}

以下のURLと関連情報を徹底的に調査してください。
{url}

【調査項目1：基本情報】
・講座名・運営者名
・価格帯（月額・年額・一括）
・受講形式（動画・ZOOM・オフライン等）
・受講期間
・受講者数・実績

【調査項目2：ターゲット分析】
・誰をターゲットにしているか
・どんな悩みに訴求しているか
・年齢・職業・レベル感

【調査項目3：カリキュラム分析】
・何を教えているか（具体的な講義内容）
・使用ツール（ChatGPT・Claude・Gemini等）
・学習のゴール・習得できるスキル
・カリキュラムの特徴・強み

【調査項目4：Level分析】
真田孔明のAI活用Level 1〜5基準で分析：
Level 1：質問・回答のみ
Level 2：プロンプト工夫・業務組み込み
Level 3：API活用・自動化
Level 4：複数AI連携・エージェント設計
Level 5：AI組織経営・完全自動化

→ この講座のゴールはLevel いくつか？
→ その根拠は何か？

【調査項目5：セールスレター分析】
・ヘッドラインの表現
・問題提起の言葉
・ベネフィットの伝え方
・価格の正当化方法
・CTAの表現

【調査項目6：真田孔明の講座との比較】
・重複している部分（避けるべき表現）
・差別化できる部分
・真田孔明の講座にないが追加できるもの
・ブレインダンプに純粋に足せる新しい表現・訴求

【調査項目7：カリキュラムの転用可能性】
・真田孔明のLevel 1→5カリキュラムに
　取り入れられる要素はあるか
・具体的にどのステップに組み込めるか

日本語で出力してください。
"""

    print(f"\n{school_id}：{school_name} を分析中...")

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

def create_integration_report(all_results):
    prompt = f"""
以下は日本の主要AI講座4校の分析結果です。

{all_results[:8000]}

この分析結果を踏まえて以下を作成してください。

【出力1：セールスレターへの追加素材】
真田孔明のセールスレターに
重複なく純粋に足せる新しい表現・訴求を
以下のパート別に20項目ずつ出力してください。

・Q（絞り込み）への追加素材
・U（共感）への追加素材
・E（教育）への追加素材
・S（刺激）への追加素材
・T（行動促進）への追加素材
・反論処理への追加素材

各項目に：
→ フレーズ例
→ WHY（なぜ有効か）
→ 差別化ポイント（他校との違い）

【出力2：カリキュラム改善提案】
真田孔明のLevel 1→5カリキュラムに
取り入れられる要素を
各Levelごとに提案してください。

Level 1→2への追加要素：
Level 2→3への追加要素：
Level 3→4への追加要素：
Level 4→5への追加要素：

【出力3：Level到達度比較表】
4校それぞれのゴールLevelと
真田孔明の講座との差別化ポイントを
一覧表で整理してください。

【出力4：真田孔明の圧倒的優位性】
4校と比較した時の
真田孔明にしかない独自の強みを
10項目以上で整理してください。
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"統合レポート生成失敗：{e}"

def main():
    os.makedirs(SAVE_DIR, exist_ok=True)

    all_results = ""
    today = datetime.now().strftime("%Y年%m月%d日")

    for school_id, school_name, url, search_query in TARGETS:
        result = analyze_school(school_id, school_name, url, search_query)

        individual_file = os.path.join(
            SAVE_DIR,
            f"{school_id}_{school_name}_分析.md"
        )
        with open(individual_file, "w") as f:
            f.write(f"# {school_id}：{school_name} 分析レポート\n")
            f.write(f"## 調査日：{today}\n\n")
            f.write(result)

        all_results += f"\n\n=== {school_name} ===\n{result}"
        print(f"✅ {school_id}：{school_name} 完了")

    print("\n統合レポートを生成中...")
    integration = create_integration_report(all_results)

    integration_file = os.path.join(
        SAVE_DIR,
        "00_日本AI講座_統合分析レポート.md"
    )
    with open(integration_file, "w") as f:
        f.write(f"# 日本AI講座4校 統合分析レポート\n")
        f.write(f"## 調査日：{today}\n")
        f.write("## 対象：機械学習・Shift AI・Life Shift Lab・ホリエモンAI学校\n\n")
        f.write("---\n\n")
        f.write(integration)

    all_file = os.path.join(SAVE_DIR, "00_全校_個別分析_統合.md")
    with open(all_file, "w") as f:
        f.write(f"# 日本AI講座4校 個別分析 全データ\n")
        f.write(f"## 調査日：{today}\n\n---\n\n")
        f.write(all_results)

    print(f"✅ 全4校の分析完了")
    print(f"✅ 統合レポート：{integration_file}")

    import subprocess
    subprocess.run([
        "bash", "-c",
        "cd ~/Desktop/AI経営本部 && "
        "git add AI活用講義/セールスレター制作/06_競合分析統合/ && "
        "git commit -m '日本AI講座4校分析完了・セールスレター追加素材・カリキュラム改善提案' && "
        "git push origin salesletter-development"
    ])

    print("✅ GitHubプッシュ完了")
    print("\n確認URL：")
    print("https://github.com/koumeisanada/ai-keiei-honbu/blob/salesletter-development/AI活用講義/セールスレター制作/06_競合分析統合/日本AI講座分析/00_日本AI講座_統合分析レポート.md")

if __name__ == "__main__":
    main()
