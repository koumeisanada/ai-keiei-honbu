from google import genai
import os
import sys

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "AIzaSyDk3qZznYlKsX6lmMUMjGrNcsqf9lrTOsI"))

def generate_reel(merumaga_text):
    prompt = f"""あなたは真田孔明のInstagramリール動画ライターです。
以下のルールを全て守って原稿を作成してください。

【絶対ルール：文字数】
・必ず200文字以上250文字以内（これより多くても少なくてもNG）
・生成後に必ず自分で文字数を数えて確認すること
・250文字を超えていたら削る、200文字未満なら足す

【文体ルール】
・です・ます調
・一人称は「僕」
・短い文で改行多め
・最初の1文で視聴者を掴む

【広告審査対応：以下は絶対に使わない】
・具体的な収益・金額の約束
・必ず・絶対に・100%などの確実性表現
・投資・融資・副業などの直接的な金融用語

【使うべき抽象的な表現】
・お金との向き合い方
・人生の設計図
・選択肢を増やす
・豊かさの本質
・働き方・生き方

【構成】
1行目：視聴者が止まる問いかけ
2〜5行：共感を呼ぶ問題提起
6〜8行：解決の方向性・ヒント
最終行：フォロー・保存・LINE登録への誘導

【重要】最後に「文字数：XX文字」と記載すること

メルマガ：
{merumaga_text[:800]}"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    merumaga_text = sys.argv[1] if len(sys.argv) > 1 else ""
    result = generate_reel(merumaga_text)
    print(result)
