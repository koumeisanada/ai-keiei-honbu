from google import genai
import os
import sys
import glob

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "AIzaSyDk3qZznYlKsX6lmMUMjGrNcsqf9lrTOsI"))

def load_past_posts():
    folder = os.path.expanduser(
        "~/Desktop/AI経営本部/集客販売/Instagram動画原稿/ゼータ/"
    )
    posts = []
    for file in sorted(glob.glob(f"{folder}*.txt"))[:10]:
        with open(file, "r", encoding="utf-8") as f:
            posts.append(f.read())
    return "\n\n---\n\n".join(posts)

def generate_reel_zeta(theme=""):
    past_posts = load_past_posts()

    prompt = f"""あなたはインスタ名「ゼータ」こと真田孔明のInstagramリール動画ライターです。

【過去の投稿（文体・世界観を完全に学習すること）】
{past_posts[:3000]}

【ゼータの世界観】
・40代ビジネスマンの心の奥底に刺さる言葉
・「三代」のような一言で世界観を作るタイトル
・知っているようで知らなかった真実を語る
・短い言葉で深い気づきを与える
・説教臭くなく共感から入る
・「大富豪のメンターに教わった」という権威付けを自然に使う
・テック比喩（OS・アプリ・バグ）や自然比喩（果樹園・航海術・嵐）を活用
・「アラフィフニート」「ネオニート」のライフスタイルを体現

【今日のテーマ】
{theme if theme else "40代ビジネスマンが思わず止まる、人生・お金・家族・継承に関するテーマを自由に選ぶ"}

【絶対ルール】
・サムネイルタイトル：1〜8文字で世界観を作る（漢字重厚語・二項対立・斜線区切りなど）
・本文：200文字以上250文字以内（厳守）
・広告審査対応：具体的金額・確実性表現・直接的な金融用語は使わない
・生成後に文字数を数えて確認すること

以下の形式で出力してください：

【サムネイルタイトル】
（ここに1〜8文字のタイトル）

【本文原稿】
（ここに200〜250文字の本文）

【文字数】XX文字

【バズりポイント】
（なぜこの原稿がバズるか一言で）"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    theme = sys.argv[1] if len(sys.argv) > 1 else ""
    result = generate_reel_zeta(theme)
    print(result)
