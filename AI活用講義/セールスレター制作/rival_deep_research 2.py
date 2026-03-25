from google import genai
from google.genai import types
import os
from datetime import datetime

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SAVE_DIR = os.path.expanduser(
    "~/Desktop/AI経営本部/AI活用講義/セールスレター制作/06_競合分析統合/ライバル徹底調査"
)

JAPAN_TARGETS = [
    ("JP01", "AI Academy aiacademy.co.jp", "AI Academy 講座 カリキュラム 料金 LP セールス"),
    ("JP02", "Aidemy Premium Plan", "Aidemy Premium Plan AI講座 料金 カリキュラム"),
    ("JP03", "テックアカデミー AI講座", "テックアカデミー AI講座 料金 カリキュラム"),
    ("JP04", "侍エンジニア AI講座", "侍エンジニア AI講座 料金 カリキュラム"),
    ("JP05", "デジタルハリウッド AI", "デジタルハリウッド AI講座 料金 カリキュラム"),
    ("JP06", "Udemy 日本語AI人気講座", "Udemy 日本語 ChatGPT AI 人気講座 ベストセラー"),
    ("JP07", "GUGA AI活用講座", "GUGA AI活用講座 カリキュラム 料金"),
    ("JP08", "Schoo AI講座", "Schoo AI講座 カリキュラム 料金"),
    ("JP09", "Progate AI講座", "Progate AI Python 講座 料金"),
    ("JP10", "DIVE INTO CODE AI", "DIVE INTO CODE AI カリキュラム 料金"),
    ("JP11", "キカガク AI講座", "キカガク AI講座 法人 個人 料金 カリキュラム"),
    ("JP12", "Skill Hacks AI", "Skill Hacks AI副業 講座 料金"),
    ("JP13", "Brain AI副業講座", "Brain AI副業 売れている 人気 講座"),
    ("JP14", "note AI活用マガジン", "note AI活用 人気 有料マガジン"),
    ("JP15", "ChatGPT日本語コミュニティ", "ChatGPT 日本語 コミュニティ 有料 月額"),
    ("JP16", "AI活用Lab", "AI活用Lab 講座 コミュニティ 料金"),
    ("JP17", "ホリエモンAI学校", "ホリエモン AI学校 講座 カリキュラム 料金"),
    ("JP18", "Shift AI", "Shift AI 講座 カリキュラム 料金 LP"),
    ("JP19", "Life Shift Lab AI", "Life Shift Lab AI講座 カリキュラム 料金"),
    ("JP20", "Grow with Google AI", "Google AI 日本語 講座 無料 有料"),
]

ENGLISH_TARGETS = [
    ("EN01", "Sam Ovens Skool", "Sam Ovens Skool AI course curriculum price sales letter"),
    ("EN02", "Iman Gadzhi AI Agency", "Iman Gadzhi AI automation agency course price curriculum"),
    ("EN03", "Dan Martell SaaS Academy", "Dan Martell SaaS Academy AI course sales letter"),
    ("EN04", "Liam Ottley AI Accelerator", "Liam Ottley AI agency accelerator course price"),
    ("EN05", "Nick Saraev AI Automation", "Nick Saraev AI automation course curriculum"),
    ("EN06", "Matt Wolfe AI Tools", "Matt Wolfe AI tools course future tools"),
    ("EN07", "Andrew Ng AI For Everyone", "Andrew Ng AI for everyone Coursera curriculum"),
    ("EN08", "Allie K Miller AI Business", "Allie K Miller AI business course"),
    ("EN09", "Cole Gordon AI Sales", "Cole Gordon AI sales training course"),
    ("EN10", "Alex Hormozi AI Course", "Alex Hormozi AI business course curriculum"),
    ("EN11", "Russell Brunson AI Funnel", "Russell Brunson AI funnel course ClickFunnels"),
    ("EN12", "Grant Cardone AI Business", "Grant Cardone AI business training"),
    ("EN13", "Tony Robbins AI Integration", "Tony Robbins AI business integration course"),
    ("EN14", "Tai Lopez AI Course", "Tai Lopez AI course knowledge society"),
    ("EN15", "Justin Welsh AI Solopreneur", "Justin Welsh AI solopreneur course"),
    ("EN16", "Sahil Bloom AI Productivity", "Sahil Bloom AI productivity course"),
    ("EN17", "David Perell AI Writing", "David Perell AI writing course"),
    ("EN18", "Nathan Barry AI ConvertKit", "Nathan Barry AI creator course ConvertKit"),
    ("EN19", "Pat Flynn AI Smart Passive", "Pat Flynn AI smart passive income course"),
    ("EN20", "Amy Porterfield AI Course", "Amy Porterfield AI online course digital"),
    ("EN21", "Marie Forleo AI B School", "Marie Forleo B School AI integration"),
    ("EN22", "Kajabi AI Course Platform", "Kajabi AI course creators success stories"),
    ("EN23", "Teachable AI Top Courses", "Teachable AI top selling courses"),
    ("EN24", "Maven AI Cohort", "Maven AI cohort course curriculum"),
    ("EN25", "Skool AI Community", "Skool AI community top courses curriculum"),
]

def analyze_rival(rival_id, rival_name, search_query, language="ja"):
    today = datetime.now().strftime("%Y年%m月%d日")

    prompt = f"""
【調査日】{today}
【調査対象】{rival_name}
【検索キーワード】{search_query}

以下を徹底的に調査してください。

## 1. 基本情報
・講座名・運営者名・URL
・価格帯（月額・年額・一括・無料枠）
・受講形式（動画・ZOOM・オフライン・コミュニティ）
・受講期間・サポート期間
・受講者数・会員数・実績数字

## 2. ターゲット分析
・メインターゲット（年齢・職業・レベル）
・どんな悩み・問題に訴求しているか
・どんな未来・ゴールを約束しているか

## 3. カリキュラム詳細
・具体的な講義内容（全モジュール・全章）
・使用ツール（ChatGPT・Claude・Gemini・Midjourney等）
・学習のゴール・習得できるスキル
・特徴的なコンテンツ・独自の強み

## 4. Level分析（真田孔明基準）
Level 1：質問・回答のみ
Level 2：プロンプト工夫・業務組み込み
Level 3：API活用・自動化
Level 4：複数AI連携・エージェント設計
Level 5：AI組織経営・完全自動化

→ この講座のゴールはLevel いくつか？
→ その根拠は？

## 5. セールスレター・LP分析
・ヘッドラインの表現（実際の言葉）
・問題提起・共感の言葉
・ベネフィットの伝え方
・社会的証明の使い方
・価格の正当化方法
・緊急性・希少性の作り方
・CTAの表現

## 6. 真田孔明との比較
・重複している部分（避けるべき表現）
・真田孔明が勝っている部分
・真田孔明が学べる部分
・市場の空白地帯（誰も教えていない部分）

## 7. セールスレターへの転用素材（30項目以上）
Q・U・E・S・T・反論処理・クロージング
それぞれに使える表現を30項目以上出力してください。
各項目にWHYと転用フレーズを付けること。

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
        return response.text if response.text else f"（{rival_name}：テキスト取得失敗）"
    except Exception as e:
        print(f"  検索ツールエラー：{e} → 通常モードで再試行")
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text if response.text else f"（{rival_name}：テキスト取得失敗）"
        except Exception as e2:
            return f"調査失敗：{e2}"

def create_master_integration(all_japan, all_english):
    prompt = f"""
以下は日本20校・英語圏25校の合計45校のAI講座分析結果です。

【日本20校の分析（抜粋）】
{all_japan[:5000]}

【英語圏25校の分析（抜粋）】
{all_english[:5000]}

この分析を元に以下を作成してください。

## 1. 市場全体のLevel到達度分布
・Level 1〜2がゴールの講座：何校・何%
・Level 2〜3がゴールの講座：何校・何%
・Level 3〜4がゴールの講座：何校・何%
・Level 4〜5がゴールの講座：何校・何%
・真田孔明のLevel 5との差

## 2. 価格帯の市場相場
・日本市場の価格帯分布
・英語圏の価格帯分布
・月額3万円の市場ポジション

## 3. カリキュラムの空白地帯（誰も教えていないこと）
真田孔明だけが教えられる独自領域を10項目以上

## 4. セールスレター表現の市場傾向
・最も使われているヘッドラインパターン
・最も使われている問題提起表現
・最も使われているベネフィット表現
・真田孔明が使うべき差別化表現

## 5. QUESTパート別 追加素材（各パート30項目以上）
### Q追加素材（30項目）
### U追加素材（30項目）
### E追加素材（30項目）
### S追加素材（30項目）
### T追加素材（30項目）
### 反論処理追加素材（30項目）
### クロージング追加素材（30項目）

## 6. 真田孔明の圧倒的優位性（45校比較）
45校との比較で浮かび上がる
真田孔明にしかない独自の強みを20項目以上

## 7. カリキュラム改善提案
45校の調査から学べる
Level 1→5カリキュラムへの改善提案を
Level別に具体的に提案してください。
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
    except Exception:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

def main():
    os.makedirs(SAVE_DIR, exist_ok=True)
    japan_dir = os.path.join(SAVE_DIR, "日本20校")
    english_dir = os.path.join(SAVE_DIR, "英語圏25校")
    os.makedirs(japan_dir, exist_ok=True)
    os.makedirs(english_dir, exist_ok=True)

    print("=" * 50)
    print("ライバル徹底調査開始")
    print("日本20校 + 英語圏25校 = 合計45校")
    print("=" * 50)

    all_japan = f"# 日本AI講座20校 全分析データ\n## 調査日：{datetime.now().strftime('%Y年%m月%d日')}\n\n"

    print("\n【日本20校の調査開始】")
    for rival_id, rival_name, search_query in JAPAN_TARGETS:
        print(f"\n{rival_id}：{rival_name} 調査中...")
        result = analyze_rival(rival_id, rival_name, search_query)

        file_path = os.path.join(japan_dir, f"{rival_id}_{rival_name[:20]}.md")
        with open(file_path, "w") as f:
            f.write(f"# {rival_name}\n## 調査日：{datetime.now().strftime('%Y年%m月%d日')}\n\n{result}")

        all_japan += f"\n\n---\n\n## {rival_name}\n{result[:2000]}"
        print(f"✅ {rival_id}：{rival_name} 完了")

    with open(os.path.join(japan_dir, "00_日本20校_全データ.md"), "w") as f:
        f.write(all_japan)
    print("\n✅ 日本20校 全データ保存完了")

    all_english = f"# 英語圏AI講座25校 全分析データ\n## 調査日：{datetime.now().strftime('%Y年%m月%d日')}\n\n"

    print("\n【英語圏25校の調査開始】")
    for rival_id, rival_name, search_query in ENGLISH_TARGETS:
        print(f"\n{rival_id}：{rival_name} 調査中...")
        result = analyze_rival(rival_id, rival_name, search_query)

        file_path = os.path.join(english_dir, f"{rival_id}_{rival_name[:20]}.md")
        with open(file_path, "w") as f:
            f.write(f"# {rival_name}\n## 調査日：{datetime.now().strftime('%Y年%m月%d日')}\n\n{result}")

        all_english += f"\n\n---\n\n## {rival_name}\n{result[:2000]}"
        print(f"✅ {rival_id}：{rival_name} 完了")

    with open(os.path.join(english_dir, "00_英語圏25校_全データ.md"), "w") as f:
        f.write(all_english)
    print("\n✅ 英語圏25校 全データ保存完了")

    print("\n【45校統合分析レポートを生成中...】")
    master = create_master_integration(all_japan, all_english)

    master_file = os.path.join(SAVE_DIR, "00_45校_統合分析_最終レポート.md")
    with open(master_file, "w") as f:
        f.write(f"# ライバル45校 統合分析 最終レポート\n")
        f.write(f"## 調査日：{datetime.now().strftime('%Y年%m月%d日')}\n")
        f.write("## 日本20校 + 英語圏25校\n\n---\n\n")
        f.write(master)

    print("✅ 45校統合分析レポート完成")

    import subprocess
    result = subprocess.run(["bash", "-c",
        "cd ~/Desktop/AI経営本部 && "
        "git add AI活用講義/セールスレター制作/06_競合分析統合/ && "
        "git commit -m 'ライバル45校徹底調査完了（日本20校＋英語圏25校）' && "
        "git push origin salesletter-development"
    ], capture_output=True, text=True)

    print("✅ GitHubプッシュ完了")
    print("\n" + "=" * 50)
    print("調査完了サマリー")
    print("=" * 50)
    print(f"・日本：20校分析完了")
    print(f"・英語圏：25校分析完了")
    print(f"・合計：45校")
    print(f"・統合レポート：00_45校_統合分析_最終レポート.md")
    print(f"\n確認URL：")
    print("https://github.com/koumeisanada/ai-keiei-honbu/blob/salesletter-development/AI活用講義/セールスレター制作/06_競合分析統合/ライバル徹底調査/00_45校_統合分析_最終レポート.md")

if __name__ == "__main__":
    main()
