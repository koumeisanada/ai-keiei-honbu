from google import genai
from google.genai import types
import os
import glob
from datetime import datetime

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SUPPLEMENT_THEMES = {
    1: "Make・Zapier・n8nを使ったAI自動化の実践",
    2: "AI×SNSマーケティングの最新手法",
    3: "AI×物販・EC自動化の具体的な方法",
    4: "プロンプトエンジニアリングの最新技法",
    5: "AI×財務・経理・確定申告の効率化",
    6: "AI×採用・HR管理の自動化",
    7: "AIエージェントの最新動向と実装方法",
    8: "AI×動画制作・編集の自動化",
    9: "AI×顧客対応・チャットボットの構築",
    10: "AI×リサーチ・情報収集の自動化",
    11: "AI×資料作成・プレゼン自動化",
    12: "AI×メール・コミュニケーション自動化",
}

def load_rival_data():
    rival_dir = os.path.expanduser(
        "~/Desktop/AI経営本部/AI活用講義/セールスレター制作/06_競合分析統合/ライバル徹底調査"
    )
    data = ""
    for f in glob.glob(f"{rival_dir}/**/*.md", recursive=True)[:5]:
        with open(f, "r") as fp:
            data += fp.read()[:1000]
    return data

def generate_supplement(month_num):
    today = datetime.now().strftime("%Y年%m月%d日")
    theme = SUPPLEMENT_THEMES.get(month_num, "AIの最新活用ノウハウ")
    rival_data = load_rival_data()

    prompt = f"""
あなたは真田孔明のAI活用講座の講師AIです。
第{month_num}ヶ月目の補足講義資料を作成してください。

【補足講義のコンセプト】
世界中のAI講座（日本20校・英語圏25校・計45校）が教えている内容の中で
真田孔明の年間プログラムに含まれていない有益なノウハウを厳選して提供する。

【今月のテーマ】{theme}
【調査日】{today}

【ライバル調査データ（参照用）】
{rival_data[:2000]}

【出力内容】

# 第{month_num}ヶ月目 補足講義：{theme}

## 今月のテーマを選んだ理由
・なぜこのテーマが重要か
・どの競合講座で教えられているか
・真田孔明の年間プログラムとの連携ポイント

## 世界の最新動向
・このテーマに関する最新情報
・世界の事例・成功例
・日本での応用可能性

## 実践ワーク（45分）
### ワーク1（15分）：
### ワーク2（15分）：
### ワーク3（15分）：

## 使用ツール・リソース
・推奨ツール一覧
・参考リンク
・次のステップ

## Level別の活用方法
・Level 1〜2の受講生向け
・Level 3〜4の受講生向け
・Level 5を目指す受講生向け

## 本日のまとめ
・今日学んだこと
・明日から使える具体的なアクション3つ
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
    import sys
    month_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    theme = SUPPLEMENT_THEMES.get(month_num, "AIの最新活用ノウハウ")
    print(f"第{month_num}ヶ月目 補足講義資料を生成中：{theme}")
    result = generate_supplement(month_num)
    save_dir = os.path.expanduser(
        "~/Desktop/AI経営本部/AI活用講義/講義資料/補足講義"
    )
    os.makedirs(save_dir, exist_ok=True)
    output_file = os.path.join(
        save_dir,
        f"第{month_num:02d}ヶ月目_補足講義_{theme[:20]}.md"
    )
    with open(output_file, "w") as f:
        f.write(result)
    print(f"✅ 保存完了：{output_file}")

if __name__ == "__main__":
    main()
