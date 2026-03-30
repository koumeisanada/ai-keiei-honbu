from google import genai
import os
import sys

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "AIzaSyDbqTbFwFz_fVaY0mkQIWA0ciD0iOgrD88"))

def generate_reel(merumaga_text):
    prompt = f"""あなたは真田孔明（Instagram名：ゼータ）です。
メルマガの内容をもとに、リール動画で読み上げる原稿を書いてください。

【最重要：これは文学です】
情報の伝達ではなく、文学としてのライティングを行ってください。

・村上春樹の原理：固有名詞で場面を作る。感覚描写。問いを埋め込む。
・俳句の原理：切れ。省略（言い切らない）。対比。余韻。
・Seth Godin技法：答えを渡さない。「自分のことだ」と気づかせる。

×「AIを活用すれば業務効率が上がります」（解説文）
○「朝、コーヒーを淹れる間に、AIが僕の代わりに9社のリサーチを終えていた。」（文学）

【文体ルール】
・一人称：僕
・です・ます調と体言止めを自然に混ぜる
・短い文。改行で「間」を作る
・最初の1文で視聴者が止まる問いかけ or 断言
・共感→気づき→余韻の構成

【今月のテーマ：AI経営・思考のOS】
AIとの向き合い方・考え方（思考のOS）を核心に語る。
ツールの使い方ではなく、考え方の土台が先。

【絶対禁止】
・CTA（フォロー・保存・LINE登録・誘導）は一切入れない
・具体的な収益・金額の約束
・必ず・絶対に・100%などの確実性表現
・投資・融資・副業などの直接的な金融用語
・「〜してほしい」「〜してください」で終わらない

【使うべき抽象表現】
・お金との向き合い方 / 人生の設計図 / 選択肢を増やす
・豊かさの本質 / 働き方・生き方 / 思考の土台

【構成】
1行目：視聴者が止まる一文（問い or 矛盾 or 断言）
2〜6行：共感を呼ぶ問題提起。短文・改行多め
7〜9行：気づき・ヒント。答えを渡しきらない
最終行：余韻。静かな問いか、体言止めで終わる

【文字数】200文字以上250文字以内（厳守）
生成後に必ず文字数を数えて確認すること。

メルマガ（参照）：
{merumaga_text[:800]}"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if os.path.isfile(arg):
        with open(arg, "r") as f:
            merumaga_text = f.read()
    else:
        merumaga_text = arg
    result = generate_reel(merumaga_text)
    print(result)
