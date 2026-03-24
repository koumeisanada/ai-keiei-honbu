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

def load_past_merumaga():
    """過去3日分のメルマガを読み込む"""
    past = ""
    for date in ["20260322", "20260323", "20260324"]:
        content = load_file(
            f"~/Desktop/AI経営本部/集客販売/日次成果物/{date}/メルマガ.txt"
        )
        if content:
            past += f"\n\n=== {date}のメルマガ ===\n{content[:1000]}"
    return past

def load_keita_materials():
    """ケイタ式の資料を読み込む"""
    import glob
    materials = ""
    files = glob.glob(
        os.path.expanduser(
            "~/Desktop/AI経営本部/物販ビジネス/ケイタ式/資料/**/*"
        ),
        recursive=True
    )
    for f in sorted(files)[:10]:
        if os.path.isfile(f):
            try:
                with open(f, "r", encoding="utf-8", errors="ignore") as fp:
                    materials += f"\n\n=== {os.path.basename(f)} ===\n{fp.read()[:500]}"
            except:
                pass
    return materials

def load_skills():
    """SKILLファイルを読み込む"""
    skill_dir = os.path.expanduser(
        "~/Desktop/AI経営本部/集客販売/メルマガ原稿"
    )
    skills = ""
    for filename in [
        "SKILL_メルマガ自動生成.md",
        "SKILL_真田孔明学習メモ.md",
    ]:
        skills += load_file(f"{skill_dir}/{filename}")
    return skills

def generate_merumaga():
    today = datetime.now().strftime("%Y年%m月%d日")
    tomorrow = "2026年3月25日（水）"
    event_date = "2026年3月28日（土）"

    skills = load_skills()
    past_merumaga = load_past_merumaga()
    keita_materials = load_keita_materials()

    prompt = f"""
あなたは真田孔明の執筆スタイルを完全に再現するAIです。

【SKILLファイル・執筆ルール】
{skills[:3000]}

【過去3日分のメルマガ（重複禁止）】
{past_merumaga[:2000]}

【ケイタ式の資料（参考）】
{keita_materials[:2000]}

【執筆指示】

明日（{tomorrow}）配信するメルマガを執筆してください。

テーマ：今週土曜日（{event_date}）開催のケイタ式イベント告知

【イベント情報】
・開催日時：2026年3月28日（土）
・内容：ケイタ式 国内仕入・海外輸出販売の実践セミナー
・告知文として自然に誘導する

【重複禁止】
過去3日分のメルマガと以下が重複しないようにすること：
・書き出しのパターン
・使用しているエピソード
・キーワード・フレーズ
・文章の切り口・テーマ

【文字数の厳守】
・合計：4,000文字（句読点・改行含む）
・序論：約1,000文字
・本論①：約1,000文字
・本論②：約1,000文字
・結論CTA：約1,000文字

【執筆ルール】
・一人称は「僕」のみ
・です・ます調を徹底
・架空の人物は登場させない
・真田孔明自身の実体験のみ
・数字は具体的に記載
・煽り表現は使わない
・感情は場面で伝える
・短文を積み重ねる
・改行を多用する
・問いかけを随所に入れる
・イベント告知はCTAパートで自然に入れる

【構成の指定】
序論：ケイタ式との出会いや印象的なエピソードから始める
本論①：国内仕入・海外輸出というビジネスモデルの本質
本論②：このビジネスで気づいた重要なこと
結論CTA：今週土曜日のイベント告知を自然な流れで

【出力形式】
件名：（メルマガの件名を先に書く）

本文：
（4,000文字のメルマガ本文）

【文字数確認】
出力前に必ず文字数をカウントして
4,000文字以上になっているか確認すること。
不足している場合は加筆してから出力すること。
"""

    print("Claudeでメルマガを執筆中...")
    message = claude_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=6000,
        messages=[{"role": "user", "content": prompt}]
    )
    result = message.content[0].text
    print("✅ 執筆完了")
    return result

def main():
    today = "20260325"
    os.makedirs(SAVE_DIR, exist_ok=True)

    print("=" * 60)
    print("ケイタ式イベント告知メルマガ執筆開始")
    print("配信予定：2026年3月25日（水）")
    print("イベント：2026年3月28日（土）")
    print("=" * 60)

    merumaga = generate_merumaga()

    output_file = os.path.join(SAVE_DIR, "メルマガ_ケイタ式イベント告知.txt")
    with open(output_file, "w") as f:
        f.write(merumaga)

    char_count = len(merumaga)
    print(f"\n✅ 保存完了：{output_file}")
    print(f"文字数：{char_count}文字")

    if char_count < 3500:
        print("⚠️ 文字数が不足しています。再生成します...")
        merumaga2 = generate_merumaga()
        with open(output_file, "w") as f:
            f.write(merumaga2)
        print(f"再生成後の文字数：{len(merumaga2)}文字")

    print("\n" + "=" * 60)
    print("✅ 完了！")
    print(f"確認先：{output_file}")
    print("=" * 60)

    import subprocess
    subprocess.run(["bash", "-c",
        "cd ~/Desktop/AI経営本部 && "
        "git add 集客販売/ && "
        "git commit -m 'ケイタ式イベント告知メルマガ執筆完了（3/25配信・3/28告知）' && "
        "git push origin main"
    ])

if __name__ == "__main__":
    main()
