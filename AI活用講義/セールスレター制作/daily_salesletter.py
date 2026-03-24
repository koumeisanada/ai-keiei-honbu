from google import genai
from google.genai import types
import os
from datetime import datetime, date

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

BASE_DIR = os.path.expanduser(
    "~/Desktop/AI経営本部/AI活用講義/セールスレター制作"
)

SCHEDULE = {
    "2026-03-21-AM": ("00_ブレインダンプ", "ターゲット分析①", "この講座を受けるべき人物像・Level 1〜5で今どこにいるか"),
    "2026-03-21-PM": ("00_ブレインダンプ", "ターゲット分析②", "ターゲットが毎日感じている痛み・不安・焦り"),
    "2026-03-22-AM": ("00_ブレインダンプ", "欲求・願望の深堀り", "ターゲットが本当に手に入れたいもの"),
    "2026-03-22-PM": ("00_ブレインダンプ", "プロジェクト名候補", "今月中に決定するプロジェクト名を20〜30案"),
    "2026-03-23-AM": ("01_Q_絞り込み", "Q①ターゲット絞り込み", "誰のための講座かを明確にする言葉"),
    "2026-03-23-PM": ("01_Q_絞り込み", "Q②資格付与", "向いている人・向いていない人"),
    "2026-03-24-AM": ("01_Q_絞り込み", "Q③共鳴フレーズ", "読者が思わず頷く絞り込みの言葉"),
    "2026-03-24-PM": ("02_U_共感", "U①現状の痛み共感", "AIに乗り遅れている恐怖・焦り"),
    "2026-03-25-AM": ("02_U_共感", "U②感情的共感", "わかってもらえたと感じる言葉"),
    "2026-03-25-PM": ("02_U_共感", "U③社会的共感", "時代・環境の変化による共感"),
    "2026-03-26-AM": ("03_E_教育", "E①なぜAI組織が必要か", "AIを道具ではなく組織として使う理由"),
    "2026-03-26-PM": ("03_E_教育", "E②なぜ今すぐなのか", "先延ばしにする危険性"),
    "2026-03-27-AM": ("03_E_教育", "E③なぜ他では学べないか", "真田孔明だけが提供できる理由"),
    "2026-03-27-PM": ("04_S_刺激", "S①理想の未来像", "講座受講後の具体的な1日"),
    "2026-03-28-AM": ("04_S_刺激", "S②感情的刺激", "自由・時間・お金が手に入った喜び"),
    "2026-03-28-PM": ("04_S_刺激", "S③対比刺激", "受講した人としなかった人の1年後"),
    "2026-03-29-AM": ("05_T_行動促進", "T①今すぐ行動する理由", "緊急性・希少性の設計"),
    "2026-03-29-PM": ("05_T_行動促進", "T②リスク除去", "不安・疑念を取り除く言葉"),
    "2026-03-30-AM": ("05_T_行動促進", "T③クロージング", "最後の背中を押す言葉"),
    "2026-03-30-PM": ("06_競合分析統合", "競合との差別化①", "日本国内ライバルとの比較"),
    "2026-03-31-AM": ("06_競合分析統合", "競合との差別化②", "米国最新AI講座との比較"),
    "2026-03-31-PM": ("06_競合分析統合", "独自価値提案USP", "真田孔明だけのUSP確立"),
    "2026-04-01-AM": ("07_価格オファー設計", "価格設計", "月額3万円・年間30万円の正当化"),
    "2026-04-01-PM": ("07_価格オファー設計", "特典・保証設計", "購買意欲を高める特典と保証"),
    "2026-04-02-AM": ("08_初稿", "セールスレター初稿①", "Q+U パート"),
    "2026-04-02-PM": ("08_初稿", "セールスレター初稿②", "E+S パート"),
    "2026-04-03-AM": ("08_初稿", "セールスレター初稿③", "T+全体統合"),
    "2026-04-03-PM": ("08_初稿", "品質チェック①", "俳句×村上春樹技法の適用確認"),
    "2026-04-04-AM": ("08_初稿", "品質チェック②", "競合比較・差別化確認"),
    "2026-04-04-PM": ("08_初稿", "修正・ブラッシュアップ", "全体修正"),
    "2026-04-05-AM": ("09_最終完成", "最終チェック", "完成版確認"),
    "2026-04-05-PM": ("09_最終完成", "セールスレター完成", "公開用最終版"),
}

QUEST_CONTEXT = """
【プロジェクト概要】
目標：年商1億円（最高3億円）
商品名：最新AI講座（正式名称今月中に決定予定）
価格：月額3万円 または 年間一括30万円
必要人数：300〜1,000人
ターゲット：40代サラリーマン・個人事業主・経営者
提供者：真田孔明（北の株式投資大学・地下ソサエティ主宰）
年間12回講義

【真田孔明の圧倒的強み】
・エンジニア経験ゼロ・営業出身・アラフィフ
・48時間でLevel 5を実現した実証済みの再現性
・AI社長＋AIマネージャーという組織構造の構築経験
・Claude・Gemini・ChatGPTの3大AI横断活用を実現
・20年間のメルマガ発信による言語化の力
・米国株投資家としての本質を見抜く目
・成功シンドロームOS＝ノウハウの土台となる思考OSの提供
・12年間のコミュニティ運営実績

【最強の集客メッセージ】
「エンジニア経験ゼロの営業出身のアラフィフが
　48時間でLevel 5に到達した。
　これはあなたにも できるという証明だ。」

【文章表現の最上位原則】
俳句の矛盾原理×村上春樹描写原理×Seth Godin問い技法
・直接言わない
・逆説と場面描写で体感させる
・読者が自分で辿り着く
・「また脅しか」と思われる表現は絶対に使わない

【絶対ルール】
・架空の実績者・成功事例は使わない
・真田孔明自身の体験・哲学で完結させる
・全ての主張にWHY（なぜ）を必ず付ける
・1項目につき20〜30の深堀りを行う
・競合分析・米国最新事例を常に参照する
・年商1億円から逆算した視点を常に持つ
"""

def get_session():
    hour = datetime.now().hour
    return "AM" if hour < 12 else "PM"

def get_past_data():
    past = []
    for folder_name in ["00_ブレインダンプ", "01_Q_絞り込み",
                        "02_U_共感", "03_E_教育", "04_S_刺激",
                        "05_T_行動促進", "06_競合分析統合",
                        "07_価格オファー設計", "08_初稿"]:
        folder_path = os.path.join(BASE_DIR, folder_name)
        if os.path.exists(folder_path):
            import glob
            for f in sorted(glob.glob(f"{folder_path}/*.md"))[-3:]:
                try:
                    with open(f, "r") as fp:
                        past.append(fp.read()[:500])
                except OSError as e:
                    print(f"⚠️ ファイル読み込みスキップ: {f} ({e})")
                    continue
    return "\n\n---\n\n".join(past[-6:]) if past else ""

def run_daily_task():
    today_str = date.today().strftime("%Y-%m-%d")
    today_display = date.today().strftime("%Y年%m月%d日")
    session = get_session()
    task_key = f"{today_str}-{session}"
    session_label = "午前" if session == "AM" else "午後"

    if task_key not in SCHEDULE:
        print(f"本日（{today_display} {session_label}）のスケジュールはありません")
        return

    folder, task_name, task_theme = SCHEDULE[task_key]
    past_data = get_past_data()

    prompt = f"""
{QUEST_CONTEXT}

【本日のタスク】
日付：{today_display}（{session_label}セッション）
フォルダ：{folder}
タスク名：{task_name}
テーマ：{task_theme}

【過去の蓄積データ（参照用・重複禁止）】
{past_data}

【調査・参照してほしい情報】
1. 日本国内のAI活用・AI副業・AI自動化系の競合セールスレター
2. 米国のAIエージェント・AI自動化講座の最新セールス表現
3. 40代サラリーマン・経営者向けの訴求方法

【文章表現の指示】
全ての出力に以下の技法を適用すること：
・俳句の矛盾原理：言いたいことの逆を使って体感させる
・村上春樹の描写原理：感情を場面で見せる
・Seth Godin技法：問いを場面の中に隠す
・直接言わない・体感させる・読者が自分で辿り着く

【出力形式】
# {task_name}（{today_display} {session_label}）

## テーマ：{task_theme}

## ブレインダンプ・深堀り（20〜30項目）
各項目に必ず「WHY（なぜこれが重要か）」を付けること
俳句的矛盾・場面描写・問いを積極的に使うこと

## セールスレターへの活用メモ
このデータをQUESTのどのパートにどう使うか

## 次のセッションへの引き継ぎメモ
次回タスクに向けて特に意識すべきこと
"""

    print(f"本日{session_label}のタスク：{task_name} を実行中...")

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

    save_folder = os.path.join(BASE_DIR, folder)
    os.makedirs(save_folder, exist_ok=True)
    output_file = os.path.join(
        save_folder,
        f"{today_str}-{session}_{task_name}.md"
    )

    with open(output_file, "w") as f:
        f.write(response.text)

    log_folder = os.path.join(BASE_DIR, "毎日の作業ログ")
    os.makedirs(log_folder, exist_ok=True)
    log_file = os.path.join(log_folder, f"{today_str}-{session}_作業ログ.md")
    with open(log_file, "w") as f:
        f.write(f"# 作業ログ {today_display}（{session_label}）\n\n")
        f.write(f"- タスク：{task_name}\n")
        f.write(f"- テーマ：{task_theme}\n")
        f.write(f"- 保存先：{output_file}\n")
        f.write(f"- 完了時刻：{datetime.now().strftime('%H:%M')}\n")

    print(f"✅ 完了：{output_file}")

if __name__ == "__main__":
    run_daily_task()
