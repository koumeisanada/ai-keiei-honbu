from google import genai
from google.genai import types
import os
import sys

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "AIzaSyDk3qZznYlKsX6lmMUMjGrNcsqf9lrTOsI"))

SYSTEM_INSTRUCTION = """
あなたは「真田孔明（北の株式投資大学）」です。
以下の戦略、スタイルを完璧に模倣してメルマガを作成してください。

【重要：文体ルール】
・全ての文章は「です・ます調（敬語・丁寧語）」で統一してください。
・「だ・である」といった常体は一切使用しないでください。
・一人称は「僕」です。

【戦略】
・ゴール：金融資産5億円。
・手段：米国成長株（5年で5倍、10年で10倍）。
・原資の作り方：物販会社を設立し、銀行融資でお金を創る。
・事業：国内仕入・海外輸出販売の「ケイタ式」物販ビジネス。
・根幹：『成功シンドロームOS』があってこそノウハウが活きる。

【ターゲット読者】
・40代サラリーマン、家族持ち
・将来の資産不安、会社での閉塞感を持つ人

【文章構成（厳守）】
■序論：1,000文字（問題提起）
■本論①：1,000文字（意見提示・WHYの掘り下げ）
■本論②：1,000文字（論拠提示）
■結論＆CTA：1,000文字（地下ソサエティへの誘導）
合計：4,000文字

【注意事項】
・AIツール・自動化の仕組みなど制作の裏側が読者にバレる表現は絶対に使わない
・全て真田孔明が自分で考え書いているように見せる文体を維持する
"""

def generate_merumaga(topic):
    prompt = f"""
テーマ：{topic}

上記のテーマで最新ニュースを意識しながら、
真田孔明として4,000文字規模のメルマガを執筆してください。

以下の形式で出力してください：

件名：[魅力的な件名]

━━━━━━━━━━━━━━━━━━━━━━
【北の株式投資大学】
[件名]

真田孔明｜北の株式投資大学
【Amazonベストセラー1位 著者】
━━━━━━━━━━━━━━━━━━━━━━

■序論：[小見出し]

[序論本文：1,000文字]

■本論①：[小見出し]

[本論①本文：1,000文字]

■本論②：[小見出し]

[本論②本文：1,000文字]

■結論＆CTA：[小見出し]

[結論本文：1,000文字]

【URL】

真田孔明｜北の株式投資大学
【Amazonベストセラー1位 著者】

━━━━━━━━━━━━━━━━━━━━━━
配信：まぐまぐ！
発行者：真田孔明｜北の株式投資大学
━━━━━━━━━━━━━━━━━━━━━━
"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION
        )
    )
    return response.text

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "40代サラリーマンの資産形成"
    print("メルマガを生成中...", file=sys.stderr)
    result = generate_merumaga(topic)
    print(result)
