from google import genai
from google.genai import types
import os
import json
import glob
from datetime import datetime

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

BASE_DIR = os.path.expanduser(
    "~/Desktop/AI経営本部/AI活用講義/セールスレター制作"
)
PROGRESS_FILE = os.path.join(BASE_DIR, "セールスレター進捗.json")
MASTER_FILE = os.path.join(BASE_DIR, "MASTER_セールスレター.md")
BRAINDUMP_DIR = os.path.join(BASE_DIR, "00_ブレインダンプ")

STEPS = [
    {
        "id": "MIND",
        "name": "マインドセット設定",
        "layer": "第1層：マインドセット",
        "folder": "00_ブレインダンプ",
        "prompt": """
BD01〜BD08の全ブレインダンプ素材を踏まえて、
このセールスレターのマインドセットを確定させてください。

出力形式：
# 第1層：マインドセット

## このレターを貫く一本の軸
（対立する二つの概念を一つ決める）

## 理想の見込み客1人
（BD01から最も刺さる人物像を1人に絞る）

## 共通の敵
（BD02から最も強い敵を1つに絞る）

## 書き手の姿勢
（売るな・救え。肩に手を置いて同じ方向を見て語る。）
"""
    },
    {
        "id": "HEADLINE",
        "name": "ヘッドライン確定",
        "layer": "第3層：ヘッドライン",
        "folder": "00_ブレインダンプ",
        "prompt": """
BD07のヘッドライン候補から最も強いものを選び、
俳句×村上春樹×Seth Godin技法で磨き上げてください。

出力形式：
# 第3層：ヘッドライン

## 最終ヘッドライン（件名）
（1つだけ選ぶ）

## 候補トップ3（理由付き）
1.
2.
3.

## なぜこのヘッドラインが最強か
"""
    },
    {
        "id": "OPENING",
        "name": "オープニング執筆",
        "layer": "第4層：オープニング",
        "folder": "08_初稿",
        "prompt": """
ヘッドラインの直後に来るオープニングを執筆してください。
4ステップで構成：
1. 社会的ニュース・データで問題提起
2. 読者の感情を代弁
3. 原因の提示
4. 希望の提示

文字数：約800〜1,000文字
文体：俳句×村上春樹×Seth Godin技法を全面適用
"""
    },
    {
        "id": "Q_QUALIFY",
        "name": "Q：絞り込み執筆",
        "layer": "第5層：QUEST本体 > Q：絞り込み",
        "folder": "01_Q_絞り込み",
        "prompt": """
BD01のターゲット人物像を元に、
「この文章はあなたのためのものだ」と気づかせるQパートを執筆。

文字数：約500〜800文字
技法：矛盾原理で「あなたのことだ」と気づかせる
"""
    },
    {
        "id": "U_UNDERSTAND",
        "name": "U：共感執筆",
        "layer": "第5層：QUEST本体 > U：共感",
        "folder": "02_U_共感",
        "prompt": """
BD01・BD02を元に、読者の痛みを代弁するUパートを執筆。

文字数：約800〜1,000文字
技法：村上春樹描写原理で感情を場面で見せる
恐怖・不満・希望の渇望の3つの感情を使う
"""
    },
    {
        "id": "E_EDUCATE",
        "name": "E：教育執筆",
        "layer": "第5層：QUEST本体 > E：教育",
        "folder": "03_E_教育",
        "prompt": """
BD02・BD04を元に、問題の根本原因と解決の方向性を教えるEパートを執筆。

文字数：約1,000〜1,500文字
使う武器：Level 1〜5の定義・AI格差の構造・成功シンドロームOS
技法：逆説で「なるほど」と気づかせる
"""
    },
    {
        "id": "S_STIMULATE",
        "name": "S：刺激執筆",
        "layer": "第5層：QUEST本体 > S：刺激",
        "folder": "04_S_刺激",
        "prompt": """
BD04・BD05を元に、「自分もこうなれる」という欲求を最大化するSパートを執筆。

文字数：約1,000〜1,500文字
使う武器：真田孔明自身の48時間Level 5体験・具体的な未来像
技法：場面描写で「手に入れた後」を体感させる
"""
    },
    {
        "id": "T_TRANSITION",
        "name": "T：行動促進執筆",
        "layer": "第5層：QUEST本体 > T：行動促進",
        "folder": "05_T_行動促進",
        "prompt": """
BD06を元に、今すぐ行動する理由を作るTパートを執筆。

文字数：約500〜800文字
使う武器：価格正当化・緊急性・希少性・リスク除去
技法：矛盾で「今すぐ」を感じさせる。煽らない。事実で伝える。
"""
    },
    {
        "id": "OBJECTION",
        "name": "反論処理執筆",
        "layer": "第7層：反論処理",
        "folder": "05_T_行動促進",
        "prompt": """
BD03を元に、読者の不安を全て取り除く反論処理セクションを執筆。

文字数：約800〜1,000文字
主要反論6パターンに全て回答する
技法：俳句的矛盾で返す + 場面描写で返す
"""
    },
    {
        "id": "PRICE",
        "name": "価格・特典・保証",
        "layer": "第6層：購買意欲を高める表現",
        "folder": "07_価格オファー設計",
        "prompt": """
BD06を元に、価格提示・特典・保証セクションを執筆。

文字数：約800〜1,000文字
月額3万円 / 年間30万円の正当化
特典・ボーナスの提示
保証の提示
"""
    },
    {
        "id": "CLOSING",
        "name": "クロージング執筆",
        "layer": "第8層：クロージング",
        "folder": "08_初稿",
        "prompt": """
BD08を元に、最後の背中を押すクロージングを執筆。

8ステップ構造：
1. 問題の要約
2. 解決策の明示
3. ベネフィット再提示
4. 反論処理の最終確認
5. 希少性・緊急性の最終強調
6. 行動指示
7. 最終フレーズ（招待型CTA）
8. 署名

文字数：約800〜1,000文字
技法：CTAは「招待」にする。押しつけではなく提案。
"""
    },
    {
        "id": "INTEGRATE",
        "name": "全体統合・初稿完成",
        "layer": "最終完成版",
        "folder": "08_初稿",
        "prompt": """
これまでの全パート（ヘッドライン〜クロージング）を
設計図の順番通りに1本のセールスレターとして統合してください。

構成順：
1. ヘッドライン
2. オープニング
3. Q：絞り込み
4. U：共感
5. E：教育
6. S：刺激
7. 価格・特典・保証
8. 反論処理
9. T：行動促進
10. クロージング

統合時の注意：
・一本の軸が全体を貫いているか確認
・パート間の接続が自然か確認
・同一表現の反復がないか確認
・全体の文字数を確認（目標：8,000〜12,000文字）
"""
    },
    {
        "id": "FINAL",
        "name": "最終品質チェック・完成",
        "layer": "最終完成版",
        "folder": "09_最終完成",
        "prompt": """
統合されたセールスレター全文を最終品質チェックし、
修正が必要な箇所を全て修正した完成版を出力してください。

チェック項目：
□ 一本の軸が全パートを貫いているか
□ QUESTの5段階が揃っているか
□ 俳句×村上春樹×Seth Godin技法が適用されているか
□ 同一表現の反復がないか
□ 煽り表現がないか
□ 数字が3つ以上入っているか
□ CTAが招待型になっているか
□ です・ます調が徹底されているか
□ 一人称が「僕」で統一されているか
□ 読み終わった後に静かに何かが残るか

出力：完成版セールスレター全文
"""
    },
]

CONTEXT = """
【AI講座セールスレター コンテキスト】
商品：最新AI講座（年間12回・月額3万円 or 年間30万円）
目標：年商1億円・300〜1,000人
ターゲット：40代サラリーマン・個人事業主・経営者
提供者：真田孔明

文章表現の最上位原則：
・俳句の矛盾原理
・村上春樹描写原理
・Seth Godin問い技法
・同一表現の反復禁止
・煽り表現は一切使わない
・CTAは「招待」にする

絶対ルール：
・架空の実績者は使わない
・全ての主張にWHYを付ける
・一本の軸を全パートで貫く
"""


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"current": 0, "completed": []}


def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def load_braindump_materials():
    materials = []
    bd_files = sorted(glob.glob(os.path.join(BRAINDUMP_DIR, "BD*.md")))
    for f in bd_files:
        with open(f, "r") as fp:
            materials.append(fp.read()[:2000])
    return "\n\n---\n\n".join(materials) if materials else ""


def load_previous_outputs(progress):
    outputs = []
    for item in progress.get("completed", []):
        filepath = item.get("file", "")
        if filepath and os.path.exists(filepath):
            with open(filepath, "r") as f:
                outputs.append(f.read()[:2000])
    return "\n\n---\n\n".join(outputs[-5:]) if outputs else ""


def update_master(progress):
    now = datetime.now().strftime("%Y年%m月%d日 %H:%M")
    total = len(STEPS)
    done = progress["current"]

    content = f"# 最新AI講座 セールスレター MASTER\n"
    content += f"## 制作開始：2026年3月19日\n"
    content += f"## 最終更新：{now}\n"
    content += f"## 進捗：{done}/{total}\n\n"
    content += "---\n\n"

    # ブレインダンプ素材集
    content += "# ブレインダンプ素材集（BD01〜BD08）\n\n"
    bd_files = sorted(glob.glob(os.path.join(BRAINDUMP_DIR, "BD*.md")))
    for f in bd_files:
        fname = os.path.basename(f).replace(".md", "")
        with open(f, "r") as fp:
            bd_content = fp.read()
        content += f"## {fname}\n\n"
        content += bd_content
        content += "\n\n---\n\n"

    # 各層の成果物
    layer_map = {}
    for item in progress.get("completed", []):
        layer = item.get("layer", "")
        filepath = item.get("file", "")
        if filepath and os.path.exists(filepath):
            with open(filepath, "r") as f:
                layer_map[layer] = f.read()

    layers = [
        "第1層：マインドセット",
        "第3層：ヘッドライン",
        "第4層：オープニング",
        "第5層：QUEST本体 > Q：絞り込み",
        "第5層：QUEST本体 > U：共感",
        "第5層：QUEST本体 > E：教育",
        "第5層：QUEST本体 > S：刺激",
        "第5層：QUEST本体 > T：行動促進",
        "第6層：購買意欲を高める表現",
        "第7層：反論処理",
        "第8層：クロージング",
        "最終完成版",
    ]

    for layer in layers:
        content += f"# {layer}\n\n"
        if layer in layer_map:
            content += layer_map[layer]
        else:
            content += "（未完了）\n"
        content += "\n\n---\n\n"

    with open(MASTER_FILE, "w") as f:
        f.write(content)

    print(f"📄 MASTER更新完了（進捗：{done}/{total}）")


def run_next_step():
    progress = load_progress()
    current = progress["current"]

    if current >= len(STEPS):
        print("✅ セールスレター全13ステップ完了！")
        update_master(progress)
        return

    step = STEPS[current]
    now = datetime.now().strftime("%Y年%m月%d日 %H:%M")

    bd_materials = load_braindump_materials()
    prev_outputs = load_previous_outputs(progress)

    prompt = f"""
{CONTEXT}

【ブレインダンプ素材（参照用）】
{bd_materials[:8000]}

【前ステップの成果物（参照用）】
{prev_outputs[:4000]}

【本ステップの指示】
ステップ：{step['name']}
レイヤー：{step['layer']}

{step['prompt']}
"""

    print(f"\nセールスレター {current + 1}/{len(STEPS)}：{step['name']}")
    print(f"レイヤー：{step['layer']}")
    print("生成中...")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
    except Exception:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

    save_folder = os.path.join(BASE_DIR, step["folder"])
    os.makedirs(save_folder, exist_ok=True)
    output_file = os.path.join(save_folder, f"SL_{step['id']}_{step['name']}.md")

    with open(output_file, "w") as f:
        f.write(f"# セールスレター：{step['name']}\n")
        f.write(f"## レイヤー：{step['layer']}\n")
        f.write(f"## 実行日時：{now}\n\n")
        f.write("---\n\n")
        f.write(response.text)

    progress["current"] = current + 1
    progress["completed"].append({
        "step": current + 1,
        "id": step["id"],
        "name": step["name"],
        "layer": step["layer"],
        "file": output_file,
        "time": now
    })
    save_progress(progress)
    update_master(progress)

    remaining = len(STEPS) - (current + 1)
    print(f"✅ 完了：{step['name']}")
    print(f"📊 進捗：{current + 1}/{len(STEPS)}（残り{remaining}ステップ）")
    print(f"📄 保存：{output_file}")
    if remaining > 0:
        next_step = STEPS[current + 1]
        print(f"📌 次：{next_step['name']}")
    print(f"▶ 次に進む：python3 salesletter_next.py")


if __name__ == "__main__":
    run_next_step()
