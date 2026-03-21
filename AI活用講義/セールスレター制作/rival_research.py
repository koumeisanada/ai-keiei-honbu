from google import genai
from google.genai import types
import os
from datetime import datetime

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

BASE_DIR = os.path.expanduser(
    "~/Desktop/AI経営本部/AI活用講義/セールスレター制作"
)

RIVAL_THEMES = [
    (
        "RIVAL01",
        "ターゲット人物像・絞り込みフレーズ",
        """
日本国内・米国・英語圏のAI講座・AI副業・AI自動化系の
セールスレター・LP・広告で使われている
「ターゲットの絞り込みフレーズ」を調査してください。

調査対象：
・日本国内のAI講座LP（note・Brain・各種LP）
・米国のAI automation course（Sam Ovens・Iman Gadzhi等）
・英語圏のAI business coaching LP

以下を20〜30個ピックアップしてください：
1. ターゲットを絞り込む冒頭フレーズ
2. 「これはあなたのための話です」的な表現パターン
3. 読者が「自分のことだ」と感じる描写
4. 向いている人・向いていない人の表現
5. 年齢・職業・状況での絞り込み表現

各項目に：
・実際の表現例（日本語・英語）
・真田孔明の講座への転用案
・WHY（なぜこの表現が刺さるか）
"""
    ),
    (
        "RIVAL02",
        "共通の敵・問題提起フレーズ",
        """
AI講座・オンラインスクールのセールスレターで使われている
「共通の敵・問題提起」の表現を調査してください。

以下を20〜30個ピックアップしてください：
1. 共通の敵の設定方法（時代・構造・競合等）
2. 問題提起の冒頭フレーズパターン
3. 「このままではどうなるか」の表現
4. 危機感を煽らずに伝える表現
5. 読者が「そうだ」と頷く社会的証拠の使い方

各項目に転用案とWHYを付けること
"""
    ),
    (
        "RIVAL03",
        "買わない理由への反論処理フレーズ",
        """
AI講座・高額オンラインスクールのセールスレターで使われている
「反論処理」の表現を調査してください。

以下を20〜30個ピックアップしてください：
1. 「難しそう」への返し方
2. 「時間がない」への返し方
3. 「高い」への返し方
4. 「自分には無理」への返し方
5. 「効果があるか不安」への返し方
6. 「今じゃなくていい」への返し方

日本・米国の実例を混在させること
各項目に転用案とWHYを付けること
"""
    ),
    (
        "RIVAL04",
        "証明・実績・権威性の表現",
        """
AI講座のセールスレターで使われている
「証明・実績・権威性」の表現を調査してください。

以下を20〜30個ピックアップしてください：
1. 実績の見せ方（数字・期間・人数）
2. 権威性の作り方（メディア掲載・著書・実績）
3. 再現性の証明方法
4. 「エンジニアでも専門家でもない人が成功」の表現
5. 受講生の声の使い方
6. 第三者証明の活用法

各項目に転用案とWHYを付けること
"""
    ),
    (
        "RIVAL05",
        "ベネフィット・理想の未来像の表現",
        """
AI講座のセールスレターで使われている
「ベネフィット・理想の未来像」の表現を調査してください。

以下を20〜30個ピックアップしてください：
1. 受講後の未来を描写するフレーズ
2. 時間・自由・お金の手に入れ方の表現
3. 場所を選ばない働き方の描写
4. 「before→after」の表現パターン
5. 感情的ベネフィットの描写
6. 具体的な数字でベネフィットを表現する方法

各項目に転用案とWHYを付けること
"""
    ),
    (
        "RIVAL06",
        "価格提示・特典・緊急性・希少性の表現",
        """
AI講座・高額オンラインスクールのセールスレターで使われている
「価格提示・特典・緊急性・希少性」の表現を調査してください。

以下を20〜30個ピックアップしてください：
1. 高額価格の正当化フレーズ
2. 「安い」と感じさせる比較の使い方
3. 特典の見せ方・積み上げ方
4. 緊急性の作り方（嘘をつかない方法）
5. 希少性の表現（本当に希少な理由）
6. 損失回避を使った価格表現

各項目に転用案とWHYを付けること
"""
    ),
    (
        "RIVAL07",
        "ヘッドライン・冒頭フレーズの表現",
        """
世界中のAI講座・オンラインスクールで使われている
「ヘッドライン・冒頭フレーズ」の実例を調査してください。

以下を20〜30個ピックアップしてください：
1. 数字を使ったヘッドライン実例
2. 問題提起型ヘッドライン実例
3. 限定・Qualify型ヘッドライン実例
4. 好奇心を刺激するヘッドライン実例
5. 英語圏で最も成功しているヘッドラインパターン
6. 日本語に転用できる英語ヘッドラインの構造

各項目に転用案とWHYを付けること
"""
    ),
    (
        "RIVAL08",
        "クロージング・CTA・招待フレーズの表現",
        """
AI講座・オンラインスクールのセールスレターで使われている
「クロージング・CTA・招待フレーズ」を調査してください。

以下を20〜30個ピックアップしてください：
1. 最後の背中を押すフレーズ実例
2. 「今すぐ行動する理由」の表現パターン
3. 申し込みボタン前後のフレーズ
4. 「招待」として表現するクロージング実例
5. 緊急性・希少性の最終強調フレーズ
6. 署名前の最後の一文パターン

各項目に転用案とWHYを付けること
"""
    ),
]

SAVE_DIR = os.path.join(BASE_DIR, "06_競合分析統合", "ライバル調査")

def research_rival_theme(theme_id, theme_name, prompt_detail):
    today = datetime.now().strftime("%Y年%m月%d日 %H:%M")

    prompt = f"""
【調査日】{today}
【調査テーマ】{theme_name}

{prompt_detail}

【重要な調査ルール】
・直近1年以内の最新情報を優先する
・日本国内と英語圏（米国・英国・豪州）両方を調査する
・実際のセールスレター・LP・広告の実例を引用する
・URLや発信者名を可能な限り明記する
・各項目には必ず以下を含める：
　- 実際の表現例
　- 真田孔明のAI講座への転用案
　- WHY（なぜこの表現が刺さるか）
・20項目以上・30項目以下で出力する
・全項目に番号をつける

【出力形式】
## {theme_id}：{theme_name} ライバル調査結果

### 日本国内ライバルの実例
（10〜15項目）

### 英語圏ライバルの実例
（10〜15項目）

### 真田孔明の講座への転用ベスト5
（上記から特に使えるものを5つ選んで★をつける）
"""

    print(f"\n{theme_id}：{theme_name} を調査中...")

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
        return f"調査失敗：{e}"

def main():
    os.makedirs(SAVE_DIR, exist_ok=True)

    all_results = "# ライバル調査 全テーマ統合結果\n"
    all_results += f"## 調査日：{datetime.now().strftime('%Y年%m月%d日')}\n\n---\n\n"

    for theme_id, theme_name, prompt_detail in RIVAL_THEMES:
        result = research_rival_theme(theme_id, theme_name, prompt_detail)

        individual_file = os.path.join(SAVE_DIR, f"{theme_id}_{theme_name}.md")
        with open(individual_file, "w") as f:
            f.write(f"# {theme_id}：{theme_name}\n\n")
            f.write(result)

        all_results += f"\n\n---\n\n{result}"
        print(f"✅ {theme_id} 完了・保存：{individual_file}")

    all_file = os.path.join(SAVE_DIR, "00_ライバル調査_全テーマ統合.md")
    with open(all_file, "w") as f:
        f.write(all_results)

    print(f"\n✅ 全8テーマのライバル調査完了")
    print(f"✅ 統合ファイル：{all_file}")

if __name__ == "__main__":
    main()
