from google import genai
from google.genai import types
import os
from datetime import datetime

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SAVE_DIR = os.path.expanduser(
    "~/Desktop/AI経営本部/AI活用講義/セールスレター制作/06_競合分析統合/他社比較分析"
)

CATEGORIES = [
    (
        "CAT01",
        "機械学習・データサイエンス系",
        """
以下の講座カテゴリを調査・分析してください。

【カテゴリ】機械学習・データサイエンス系
【代表的な講座】
・機械学習 kikagaku.ai
・Aidemy Premium Plan
・テックアカデミー AI講座
・DIVE INTO CODE
・データサイエンティスト養成系全般

【分析項目】
1. このカテゴリの共通的な特徴
   ・何を教えているか
   ・誰をターゲットにしているか
   ・価格帯
   ・期間
   ・Level（真田孔明基準）

2. このカテゴリで学べること・学べないこと
   ・学べること（強み）
   ・学べないこと（弱み）
   ・修了後に何ができるか

3. こんな人に向いている
   ・理想的な受講者像

4. こんな人には向いていない
   ・向いていない人の特徴

5. 真田孔明の講座との比較
   ・根本的な違い
   ・真田孔明の講座が優れている点
   ・真田孔明の講座で補完できる点

6. セールスレターQ&A形式での言語化
   Q：「機械学習の勉強をしたほうがいいのでは？」
   A：（真田孔明の答え）

   Q：「Pythonが学べないのでは？」
   A：（真田孔明の答え）

   （このカテゴリに関するQ&Aを10個以上）

7. セールスレターへの転用フレーズ（20個以上）
   各フレーズにWHYを付けること
"""
    ),
    (
        "CAT02",
        "AI副業・収益化系",
        """
【カテゴリ】AI副業・収益化系
【代表的な講座】
・Brain AI副業講座
・note AI活用マガジン
・Skill Hacks AI
・AI副業系YouTube・SNS講座全般
・英語圏のAI side hustle系コース

【分析項目】
1. このカテゴリの共通的な特徴
2. 学べること・学べないこと
3. こんな人に向いている
4. こんな人には向いていない
5. 真田孔明の講座との比較
6. セールスレターQ&A形式（10個以上）
   Q：「AI副業で稼ぐ方法を教えてくれるの？」
   A：
   Q：「月収○○万円になれる？」
   A：
7. セールスレターへの転用フレーズ（20個以上）
"""
    ),
    (
        "CAT03",
        "ChatGPT・ツール活用系",
        """
【カテゴリ】ChatGPT・ツール活用系
【代表的な講座】
・Udemy ChatGPT人気講座
・ホリエモンAI学校
・Shift AI
・ChatGPT活用系YouTube・SNS講座全般
・英語圏のChatGPT masterclass系

【分析項目】
1. このカテゴリの共通的な特徴
2. 学べること・学べないこと
3. こんな人に向いている
4. こんな人には向いていない
5. 真田孔明の講座との比較
6. セールスレターQ&A形式（10個以上）
   Q：「ChatGPTの使い方はYouTubeで無料で学べるのでは？」
   A：
   Q：「Shift AIやホリエモンAI学校とどう違うの？」
   A：
7. セールスレターへの転用フレーズ（20個以上）
"""
    ),
    (
        "CAT04",
        "AI業務効率化・DX推進系",
        """
【カテゴリ】AI業務効率化・DX推進系
【代表的な講座】
・Life Shift Lab AI
・AI Academy
・デジタルハリウッド AI
・法人向けAI研修全般
・英語圏のAI for business系

【分析項目】
1. このカテゴリの共通的な特徴
2. 学べること・学べないこと
3. こんな人に向いている
4. こんな人には向いていない
5. 真田孔明の講座との比較
6. セールスレターQ&A形式（10個以上）
   Q：「会社でAI導入を推進したいのだが？」
   A：
   Q：「DX推進担当者向けの内容はあるの？」
   A：
7. セールスレターへの転用フレーズ（20個以上）
"""
    ),
    (
        "CAT05",
        "AIエージェント・自動化系",
        """
【カテゴリ】AIエージェント・自動化系
【代表的な講座】
・Liam Ottley AI Agency Accelerator
・Nick Saraev AI Automation
・Sam Ovens Skool AI
・英語圏のAI automation agency系全般
・n8n・Make・Zapier活用系

【分析項目】
1. このカテゴリの共通的な特徴
2. 学べること・学べないこと
3. こんな人に向いている
4. こんな人には向いていない
5. 真田孔明の講座との比較
6. セールスレターQ&A形式（10個以上）
   Q：「Make・Zapierで自動化を学べるの？」
   A：
   Q：「AIエージェントの構築方法は学べるの？」
   A：
7. セールスレターへの転用フレーズ（20個以上）
"""
    ),
    (
        "CAT06",
        "AI×マーケティング・セールス系",
        """
【カテゴリ】AI×マーケティング・セールス系
【代表的な講座】
・Russell Brunson AI Funnel
・Amy Porterfield AI Course
・Marie Forleo B School AI
・英語圏のAI marketing系全般
・日本のAI×集客・SNS系講座

【分析項目】
1. このカテゴリの共通的な特徴
2. 学べること・学べないこと
3. こんな人に向いている
4. こんな人には向いていない
5. 真田孔明の講座との比較
6. セールスレターQ&A形式（10個以上）
   Q：「集客・マーケティングへのAI活用は学べる？」
   A：
   Q：「セールスレターをAIで書く方法は？」
   A：
7. セールスレターへの転用フレーズ（20個以上）
"""
    ),
    (
        "CAT07",
        "AI×投資・資産形成系",
        """
【カテゴリ】AI×投資・資産形成系
【代表的な講座】
・AI×株式投資系講座全般
・AI×不動産投資系
・AI×仮想通貨系
・英語圏のAI investing系

【分析項目】
1. このカテゴリの共通的な特徴
2. 学べること・学べないこと
3. こんな人に向いている
4. こんな人には向いていない
5. 真田孔明の講座との比較
   ※真田孔明は投資家としてAI企業を研究している点を強調
6. セールスレターQ&A形式（10個以上）
   Q：「AIで株式投資の判断を自動化できる？」
   A：
   Q：「投資とAI活用はどう関係するの？」
   A：
7. セールスレターへの転用フレーズ（20個以上）
"""
    ),
    (
        "CAT08",
        "総合比較・真田孔明の独自ポジション",
        """
【カテゴリ】全カテゴリ総合比較

以下の7カテゴリを横断して比較分析してください。
CAT01：機械学習・データサイエンス系
CAT02：AI副業・収益化系
CAT03：ChatGPT・ツール活用系
CAT04：AI業務効率化・DX推進系
CAT05：AIエージェント・自動化系
CAT06：AI×マーケティング・セールス系
CAT07：AI×投資・資産形成系

【出力内容】

1. 市場全体の俯瞰図
   各カテゴリの位置づけ・ターゲット・Level到達度

2. 真田孔明の講座が属するカテゴリ
   どのカテゴリとも違う独自ポジションの確立

3. 受講者の「よくある質問」を全カテゴリ横断で20個以上
   各カテゴリとの比較Q&A形式で

4. 真田孔明の講座を選ぶべき人・選ばなくてよい人
   正直な比較表

5. セールスレターの「他社との比較」パートの完全文章
   Q&A形式で全疑問に答える形で
   （そのままセールスレターに使える文章として）

6. セールスレターへの転用フレーズ（30個以上）
"""
    ),
]

def analyze_category(cat_id, cat_name, prompt_detail):
    today = datetime.now().strftime("%Y年%m月%d日")

    prompt = f"""
【調査日】{today}
【分析カテゴリ】{cat_name}

{prompt_detail}

【重要ルール】
・真田孔明のAI講座との比較を常に意識する
・他社を批判するのではなく事実として比較する
・Q&A形式では真田孔明の視点・言葉で答える
・セールスレターにそのまま使える文章を書く
・です・ます調を徹底する
・一人称は「僕」
・架空の実績は使わない
・日本語で出力する

【真田孔明の基本情報】
・エンジニア経験ゼロ・営業出身・アラフィフ
・48時間でLevel 5（AI組織経営）を実現
・Claude・Gemini・ChatGPTの3大AI横断活用
・AI社長＋AIマネージャー組織を構築
・月2回・年間24回の講義
・ZOOM＋オフライン両方対応
・月額3万円 or 年間30万円
・世界45校のAI講座の補足ノウハウも提供
"""

    print(f"\n{cat_id}：{cat_name} 分析中...")

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
        print(f"  検索エラー：{e} → 通常モードで再試行")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

def main():
    os.makedirs(SAVE_DIR, exist_ok=True)
    today = datetime.now().strftime("%Y年%m月%d日")

    all_results = f"# 他社講座カテゴリ比較分析 全データ\n## 調査日：{today}\n\n---\n\n"

    for cat_id, cat_name, prompt_detail in CATEGORIES:
        result = analyze_category(cat_id, cat_name, prompt_detail)

        file_path = os.path.join(SAVE_DIR, f"{cat_id}_{cat_name}.md")
        with open(file_path, "w") as f:
            f.write(f"# {cat_id}：{cat_name}\n## 調査日：{today}\n\n---\n\n{result}")

        all_results += f"\n\n---\n\n## {cat_name}\n\n{result}"
        print(f"✅ {cat_id}：{cat_name} 完了")

    all_file = os.path.join(SAVE_DIR, "00_全カテゴリ比較_統合.md")
    with open(all_file, "w") as f:
        f.write(all_results)

    qa_file = os.path.join(SAVE_DIR, "01_セールスレター用Q&A集.md")
    qa_prompt = f"""
以下の全カテゴリ比較分析から
セールスレターの「よくある質問・Q&A」パートを
完全な文章として作成してください。

{all_results[:8000]}

【出力形式】

# よくある質問

## 他の講座との比較について

Q1：機械学習やPythonを学べる講座とどう違うの？
A：

Q2：ChatGPTの使い方を教える講座は無料でもあるのでは？
A：

Q3：AI副業で稼ぐ方法を教えてくれるの？
A：

Q4：ホリエモンAI学校やShift AIとどう違うの？
A：

Q5：英語圏の安いAI講座でよくないの？
A：

（以上のような形式で20個以上のQ&Aを作成する）

【文章ルール】
・です・ます調
・一人称は「僕」
・正直に・事実として答える
・他社を批判しない
・真田孔明の講座の強みを自然に伝える
・そのままセールスレターに貼り付けられる文章
"""

    try:
        qa_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=qa_prompt
        ).text
    except Exception:
        qa_response = "Q&A生成失敗"

    with open(qa_file, "w") as f:
        f.write(f"# セールスレター用 Q&A集\n## 作成日：{today}\n\n---\n\n{qa_response}")

    print(f"\n✅ 全8カテゴリ比較分析完了")
    print(f"✅ Q&A集も自動生成完了")

    import subprocess
    subprocess.run(["bash", "-c",
        "cd ~/Desktop/AI経営本部 && "
        "git add AI活用講義/セールスレター制作/06_競合分析統合/ && "
        "git commit -m '他社講座カテゴリ比較分析・Q&A集生成完了' && "
        "git push origin salesletter-development"
    ])

    print("✅ GitHubプッシュ完了")
    print("\n確認URL：")
    print("https://github.com/koumeisanada/ai-keiei-honbu/blob/salesletter-development/AI活用講義/セールスレター制作/06_競合分析統合/他社比較分析/01_セールスレター用Q%26A集.md")

if __name__ == "__main__":
    main()
