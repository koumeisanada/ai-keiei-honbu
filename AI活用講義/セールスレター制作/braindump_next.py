from google import genai
from google.genai import types
import os
import json
from datetime import datetime

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

BASE_DIR = os.path.expanduser(
    "~/Desktop/AI経営本部/AI活用講義/セールスレター制作"
)
PROGRESS_FILE = os.path.join(BASE_DIR, "ブレインダンプ進捗.json")
BRAINDUMP_DIR = os.path.join(BASE_DIR, "00_ブレインダンプ")

BRAINDUMP_STEPS = [
    (
        "BD01",
        "理想のターゲット1人の人物像",
        """
AI講座を買う理想の見込み客を1人だけ具体的に描写する。

深堀り項目（20〜30個）：
・年齢・職業・家族構成・年収・資産状況
・毎朝起きた時に感じること
・AIについて今どう思っているか
・Level 1〜4のどこにいるか
・何に時間を一番使っているか
・何に一番お金を使っているか
・夜眠れない時に何を考えているか
・3年後にどうなっていたいか
・何が怖いか・何が恥ずかしいか
・誰に相談できないでいるか
・今まで試して失敗したこと
・なぜAI講座を買わない理由を言い訳するか
・何があれば行動できるか
・真田孔明に何を求めているか
・この人が「これは自分のことだ」と思う言葉は何か
（以上を全て20〜30項目で深堀りすること）
"""
    ),
    (
        "BD02",
        "共通の敵の定義",
        """
読者と一緒に戦う「共通の敵」を深堀りする。

深堀り項目（20〜30個）：
・AI講座ターゲットにとっての共通の敵は何か
・「AIに乗り遅れる恐怖」を具体的な場面で描写する
・「技術格差」が広がる具体的なシナリオ
・Level 1止まりが続くとどうなるか（1年後・3年後・5年後）
・敵は「人」ではなく「構造・仕組み・時代」として表現する
・読者が「そうだ、これが問題だ」と頷く言葉
・共通の敵を俳句的矛盾で表現する5パターン
・村上春樹的な場面描写で敵を表現する3パターン
（以上を全て20〜30項目で深堀りすること）
"""
    ),
    (
        "BD03",
        "買わない理由と反論処理",
        """
見込み客が買わない理由を全て洗い出し反論処理する。

深堀り項目（20〜30個）：
・「技術的に難しそう」という反論への答え
・「時間がない」という反論への答え
・「自分には無理」という反論への答え
・「高い」という反論への答え
・「本当に効果があるか」という反論への答え
・「今じゃなくていい」という反論への答え
・「他で学べる」という反論への答え
・各反論を俳句的矛盾で返す表現
・各反論を場面描写で返す表現
・反論処理のWHY（なぜこの答えが正しいか）
（以上を全て20〜30項目で深堀りすること）
"""
    ),
    (
        "BD04",
        "証明・実績・保証",
        """
セールスレターで使える証明・実績・保証を深堀りする。

深堀り項目（20〜30個）：
・エンジニアゼロ・48時間・Level 5の事実を具体的に
・Level 1から始まった具体的なプロセス
・再現性の証明（なぜ誰でもできるか）
・20年間メルマガ発信の蓄積が何を証明するか
・3大AI連携の具体的な成果
・AI経営本部構築の具体的な数字
・保証として約束できること
・「天才だからではない」という逆説の証明
・権威性（Amazonベストセラー・コミュニティ運営実績）
（以上を全て20〜30項目で深堀りすること）
"""
    ),
    (
        "BD05",
        "ベネフィット・理想の未来像",
        """
受講後に手に入るものを全て深堀りする。

深堀り項目（20〜30個）：
・受講後の具体的な朝の場面
・受講後の具体的な午後の場面
・受講後の具体的な夜の場面
・1年後の景色を村上春樹的に描写
・「時間が増えた」を場面で描写
・「場所を選ばない」を場面で描写
・Level 5になった後に何ができるか
・5ポケッツ戦略術とAIが組み合わさった未来
・家族への影響・周りへの影響
・「受講した人」と「しなかった人」の対比
（以上を全て20〜30項目で深堀りすること）
"""
    ),
    (
        "BD06",
        "価格・特典・緊急性・希少性",
        """
オファー設計のための深堀り。

深堀り項目（20〜30個）：
・月額3万円がなぜ安いかの論拠
・年間30万円がなぜ安いかの論拠
・競合と比べた価格の正当化
・特典として提供できるもの
・緊急性の作り方（嘘をつかない・事実ベース）
・希少性の作り方（本当に希少な理由）
・「今すぐ行動する理由」を俳句的矛盾で表現
・損失回避（買わないことのコスト）
・価格提示の最適なタイミングと言い方
（以上を全て20〜30項目で深堀りすること）
"""
    ),
    (
        "BD07",
        "ヘッドライン候補の深堀り",
        """
セールスレターの冒頭を飾るヘッドラインを深堀りする。

深堀り項目（20〜30個）：
・数字＋ベネフィット型を10パターン
・問題提起型を5パターン
・Qualify型（限定）を5パターン
・俳句的矛盾を使ったヘッドラインを10パターン
・各ヘッドラインのWHY（なぜ読者が止まるか）
・最も刺さると思う上位3つを選んで理由を述べる
（以上を全て20〜30項目で深堀りすること）
"""
    ),
    (
        "BD08",
        "クロージングフレーズの深堀り",
        """
最後の背中を押すフレーズを深堀りする。

深堀り項目（20〜30個）：
・「招待」として表現するクロージングを10パターン
・緊急性を煽らず事実として伝えるフレーズを5パターン
・Seth Godin的な問いで締めるフレーズを5パターン
・「人生を動かすのは今この瞬間」の言い換えを10パターン
・署名・URLの前の最後の一文を5パターン
・各フレーズのWHY（なぜこれが最後に刺さるか）
（以上を全て20〜30項目で深堀りすること）
"""
    ),
]

CONTEXT = """
【AI講座セールスレター ブレインダンプ用コンテキスト】

商品：最新AI講座（年間12回・月額3万円 or 年間30万円）
目標：年商1億円・300〜1,000人
ターゲット：40代サラリーマン・個人事業主・経営者

差別化：
・エンジニア経験ゼロの営業出身アラフィフが48時間でLevel 5
・世界中でこの技法でAI講座を売っている人間がいない
・俳句×村上春樹×Seth Godin技法による独自の文章世界観

Level 1〜5の定義：
Level 1（約80%）：質問・回答のみ
Level 2（約15%）：プロンプト工夫・業務組み込み
Level 3（約4%）：API活用・自動化
Level 4（約0.9%）：複数AI連携・エージェント設計
Level 5（約0.1%）：AI組織経営・完全自動化

文章表現の最上位原則：
・俳句の矛盾原理：言いたいことの逆で体感させる
・村上春樹描写原理：感情を場面で見せる
・Seth Godin技法：問いを場面の中に隠す
・同一表現の反復禁止
・煽り表現は一切使わない

絶対ルール：
・架空の実績者は使わない
・真田孔明自身の体験で完結させる
・全ての主張にWHYを付ける
"""

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"current": 0, "completed": []}

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def run_next_step():
    progress = load_progress()
    current = progress["current"]

    if current >= len(BRAINDUMP_STEPS):
        print("✅ ブレインダンプ全8テーマ完了！")
        print("次のステップ：salesletter_next.pyでセールスレターを書き始めてください。")
        return

    step_id, step_name, step_theme = BRAINDUMP_STEPS[current]
    now = datetime.now().strftime("%Y年%m月%d日 %H:%M")

    os.makedirs(BRAINDUMP_DIR, exist_ok=True)

    prompt = f"""
{CONTEXT}

【ブレインダンプテーマ】
ID：{step_id}
テーマ：{step_name}

【深堀り指示】
{step_theme}

【出力形式】
## {step_id}：{step_name}

### ブレインダンプ（20〜30項目）
必ず20項目以上・30項目以下で出力すること。
各項目は以下の形式で：

[番号]. [項目内容]
　→ WHY：[なぜこれが重要か・セールスレターでどう使うか]
　→ フレーズ例：[実際に使えるセールスレターの言葉]

### このテーマの核心フレーズ（3つ）
セールスレターで最も使えると思う表現を3つ選んで★をつける。

### 次のテーマへの引き継ぎメモ
このテーマで発見した重要な気づきを1〜3行で。
"""

    print(f"\nブレインダンプ {current + 1}/{len(BRAINDUMP_STEPS)}：{step_name}")
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

    output_file = os.path.join(
        BRAINDUMP_DIR,
        f"{step_id}_{step_name}.md"
    )

    with open(output_file, "w") as f:
        f.write(f"# ブレインダンプ：{step_name}\n")
        f.write(f"## 実行日時：{now}\n\n")
        f.write("---\n\n")
        f.write(response.text)

    progress["current"] = current + 1
    progress["completed"].append({
        "step": current + 1,
        "id": step_id,
        "name": step_name,
        "time": now
    })
    save_progress(progress)

    remaining = len(BRAINDUMP_STEPS) - (current + 1)
    print(f"✅ 完了：{step_name}")
    print(f"📊 進捗：{current + 1}/{len(BRAINDUMP_STEPS)}（残り{remaining}テーマ）")
    print(f"📄 保存：{output_file}")
    if remaining > 0:
        next_step = BRAINDUMP_STEPS[current + 1]
        print(f"📌 次：{next_step[1]}")
    print(f"▶ 次に進む：python3 braindump_next.py")

if __name__ == "__main__":
    run_next_step()
