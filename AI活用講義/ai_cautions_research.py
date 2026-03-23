from google import genai
from google.genai import types
import os
from datetime import datetime

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SAVE_DIR = os.path.expanduser(
    "~/Desktop/AI経営本部/AI活用講義/講義資料"
)

def research_ai_cautions():
    today = datetime.now().strftime("%Y年%m月%d日")

    prompt = f"""
【調査日】{today}

日本・米国・英語圏の以下の情報源から
「AIを活用する際にやってはいけないこと・
注意すべきこと」を徹底的に調査してください。

【調査対象】
・AI研究機関・大学の発表（MIT・スタンフォード・東大等）
・政府・公的機関の発表（総務省・経産省・EU AI規制・米国NIST等）
・AI企業の公式ガイドライン（Anthropic・OpenAI・Google等）
・ビジネス現場での失敗事例・トラブル事例
・法律・著作権・プライバシー関連の注意事項
・セキュリティ・情報漏洩リスク
・AI特有の誤りやすいポイント（ハルシネーション等）

【カテゴリ別に分類して出力してください】

## カテゴリ1：情報セキュリティ・機密情報
## カテゴリ2：著作権・知的財産
## カテゴリ3：ハルシネーション（AIの嘘）
## カテゴリ4：プライバシー・個人情報
## カテゴリ5：ビジネス上のリスク
## カテゴリ6：AI出力の品質管理
## カテゴリ7：法的リスク・規制
## カテゴリ8：心理的・認知的リスク
## カテゴリ9：ビジネス倫理・社会的責任
## カテゴリ10：実務上のよくある間違い

【各項目の出力形式】
### 注意事項のタイトル
・具体的な内容
・なぜ問題なのか（根拠・データ）
・実際の事例（あれば）
・正しい対処法
・Level別の重要度（Level 1〜5のどの段階で特に注意すべきか）

最低50項目以上を目標にすること。
日本語で出力すること。
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

def create_lecture_content(cautions_data):
    today = datetime.now().strftime("%Y年%m月%d日")

    prompt = f"""
以下のAI注意事項データを元に
真田孔明のAI活用講座の講義資料を作成してください。

{cautions_data[:6000]}

【講義の位置づけ】
・第1回講義の後半（全体像の説明の後）
・または第2回講義の冒頭
・受講生がLevel 1→5を目指す前に
　必ず知っておくべき基礎知識として

【文章スタイル：講義・セミナー用スタイルを適用】
・全ての主張に客観的な根拠・データを付ける
・結論→根拠→事実→応用の順で書く
・設計図・フレームワーク・ステップ形式を使う
・感情訴求は使わない
・論理性・根拠・データで受講生を動かす
・文学スキル（俳句・村上春樹等）は使わない

【出力内容】

# AIと向き合う前に知っておくべきこと
## 〜やってはいけないこと・注意すべきこと〜

### はじめに（全体像）
なぜこの講義が必要か（根拠：統計データ・事例付き）

### 第1章：情報セキュリティの鉄則
### 第2章：著作権・知的財産の基本
### 第3章：ハルシネーションへの対処法
### 第4章：プライバシー・個人情報の取り扱い
### 第5章：ビジネス上のリスク管理
### 第6章：AI出力の品質管理
### 第7章：法的リスク・規制への対応
### 第8章：実務でよくある間違いTOP10

### まとめ：AIと安全に向き合うための10の鉄則
### 受講生向けチェックリスト
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
    today = datetime.now().strftime("%Y年%m月%d日")

    print("AIの注意事項をリサーチ中...")
    cautions = research_ai_cautions()

    cautions_file = os.path.join(
        SAVE_DIR,
        "AI注意事項_リサーチデータ.md"
    )
    with open(cautions_file, "w") as f:
        f.write(f"# AI活用 注意事項リサーチデータ\n")
        f.write(f"## 調査日：{today}\n\n---\n\n")
        f.write(cautions)
    print(f"✅ リサーチデータ保存完了")

    print("講義資料を生成中...")
    lecture = create_lecture_content(cautions)

    lecture_dir = os.path.join(SAVE_DIR, "第01回")
    os.makedirs(lecture_dir, exist_ok=True)

    lecture_file = os.path.join(
        lecture_dir,
        "AIと向き合う前に知っておくべきこと.md"
    )
    with open(lecture_file, "w") as f:
        f.write(f"# AIと向き合う前に知っておくべきこと\n")
        f.write(f"## 〜やってはいけないこと・注意すべきこと〜\n")
        f.write(f"## 作成日：{today}\n\n---\n\n")
        f.write(lecture)
    print(f"✅ 講義資料保存完了：{lecture_file}")

    import subprocess
    subprocess.run(["bash", "-c",
        "cd ~/Desktop/AI経営本部 && "
        "git add AI活用講義/ && "
        "git commit -m 'AI注意事項講義資料生成完了（第1回講義）' && "
        "git push origin salesletter-development"
    ])
    print("✅ GitHubプッシュ完了")
    print(f"\n確認URL：")
    print("https://github.com/koumeisanada/ai-keiei-honbu/blob/salesletter-development/AI活用講義/講義資料/第01回/AIと向き合う前に知っておくべきこと.md")

if __name__ == "__main__":
    main()
