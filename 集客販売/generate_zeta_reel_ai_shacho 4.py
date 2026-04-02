import os
import anthropic
from datetime import datetime

claude_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SAVE_DIR = os.path.expanduser(
    "~/Desktop/AI経営本部/集客販売/日次成果物/20260325"
)

def load_file(path):
    try:
        with open(os.path.expanduser(path), "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except:
        return ""

def load_past_reels():
    import glob
    past = ""
    files = sorted(glob.glob(
        os.path.expanduser(
            "~/Desktop/AI経営本部/集客販売/日次成果物/*/リール動画原稿.txt"
        )
    ))[-5:]
    for f in files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as fp:
                past += f"\n\n=== {f} ===\n{fp.read()[:300]}"
        except:
            pass
    return past

def generate_reel():
    skill = load_file(
        "~/Desktop/AI経営本部/集客販売/Instagram動画原稿/ゼータ/SKILL_ゼータリール専用.md"
    )
    memo = load_file(
        "~/Desktop/AI経営本部/集客販売/メルマガ原稿/SKILL_真田孔明学習メモ.md"
    )
    past_reels = load_past_reels()

    prompt = f"""
あなたは真田孔明（ゼータ）のInstagramリール原稿を書く専門家です。

【SKILLファイル】
{skill[:2000]}

【真田孔明学習メモ】
{memo[:1000]}

【過去のリール原稿（重複禁止）】
{past_reels[:1000]}

【執筆指示】

アカウント名：アラフィフニートゼータ
テーマ：AIが社長になって複数の事業を同時に遂行できる時代が到来した

【このリールで伝えること】
・AIを「使う」時代から「社長として経営させる」時代になった
・1人でも複数の事業を同時に動かせるようになった
・真田孔明自身がその状態を実現している（実証済みの話）
・アラフィフでも・エンジニアじゃなくても実現できる

【構成の指定】
①サムネイルタイトル：（画面に大きく表示される一言）
②本文：（200〜250文字・リール動画のナレーション原稿）

【文章ルール】
・一人称は「僕」
・です・ます調
・短文を積み重ねる
・改行を多用する
・架空の事例は使わない・真田孔明自身の実体験のみ
・煽り表現は使わない
・感情は場面で伝える
・問いかけを入れる
・CTAは入れない（別途コメント欄で案内するため）
・絵文字は使わない
・過去のリールと書き出し・切り口・フレーズが重複しない

【サムネイルタイトルの条件】
・10文字以内
・思わず止まってしまう言葉
・「AIが社長」という概念を示唆する
・ネガティブな言葉は使わない

【本文の条件】
・冒頭3秒で視聴者を止める言葉から始める
・真田孔明が実際にやっていることを具体的に語る
・「AIが社長として動いている」という事実を場面で見せる
・最後に問いかけで終わる
・200文字以上250文字以内で必ず収める

【出力形式】
---サムネイルタイトル---
（タイトルを記載）

---本文---
（本文を記載）

---文字数---
（本文の文字数を記載）
"""

    print("Claudeでリール原稿を執筆中...")
    message = claude_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def main():
    today = datetime.now().strftime("%Y年%m月%d日")
    os.makedirs(SAVE_DIR, exist_ok=True)

    print("=" * 60)
    print("ゼータ Instagramリール原稿生成")
    print(f"テーマ：AIが社長になって複数事業を遂行できる時代")
    print(f"生成日：{today}")
    print("=" * 60)

    result = generate_reel()

    output_file = os.path.join(
        SAVE_DIR,
        "リール_AIが社長になった時代.txt"
    )
    with open(output_file, "w") as f:
        f.write(f"# ゼータ Instagramリール原稿\n")
        f.write(f"# テーマ：AIが社長になって複数事業を遂行できる時代\n")
        f.write(f"# 生成日：{today}\n\n")
        f.write(result)

    print(f"\n✅ 保存完了：{output_file}")
    print("\n" + "=" * 60)
    print(result)
    print("=" * 60)

    import subprocess
    subprocess.run(["bash", "-c",
        "cd ~/Desktop/AI経営本部 && "
        "git add 集客販売/ && "
        "git commit -m 'ゼータリール：AIが社長になった時代（2026年3月25日）' && "
        "git push origin main"
    ])

if __name__ == "__main__":
    main()
