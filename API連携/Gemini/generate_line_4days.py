from google import genai
import os
import sys

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "AIzaSyDk3qZznYlKsX6lmMUMjGrNcsqf9lrTOsI"))

def generate_line_4days(merumaga_text):
    parts = ["序論（問題提起）", "本論①（意見提示）", "本論②（論拠提示）", "結論＆CTA"]
    results = []

    for i, part in enumerate(parts):
        prompt = f"""あなたは真田孔明（北の株式投資大学）のLINEメッセージライターです。
以下のメルマガ原稿の{part}部分を
LINEステップメール用に900〜1000文字でリライトしてください。

ルール：
・です・ます調を徹底
・一人称は「僕」
・改行多め・1文短め
・時事ネタは普遍的な表現に変換（年号削除・季節表現削除）
・エバーグリーンな内容にする
・1行目は読者が続きを読みたくなる一文にする
・{"次回への期待感で締める" if i < 3 else "地下ソサエティへのCTAで締める"}

メルマガ全文：
{merumaga_text}

上記メルマガの{part}に対応するLINE原稿を作成してください。"""

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        results.append(f"=== LINE {i+1}通目（{part}） ===\n\n{response.text}\n\n")

    return "\n".join(results)

if __name__ == "__main__":
    merumaga_text = sys.argv[1] if len(sys.argv) > 1 else ""
    result = generate_line_4days(merumaga_text)
    print(result)
