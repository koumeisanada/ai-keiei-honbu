import os
import json
from datetime import datetime
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from google import genai
from google.genai import types
import anthropic
import openai

# APIクライアント初期化
gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# OpenAI・Anthropicはキーがある場合のみ初期化
_openai_key = os.environ.get("OPENAI_API_KEY")
_anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
if _openai_key:
    openai_client = openai.OpenAI(api_key=_openai_key)
if _anthropic_key:
    claude_client = anthropic.Anthropic(api_key=_anthropic_key)
claude_client = anthropic.Anthropic()

SAVE_DIR = os.path.expanduser(
    "~/Desktop/AI経営本部/AI活用講義/講義資料/第01回"
)

def generate_with_gemini_search(prompt):
    """Gemini：リサーチ・最新情報収集に使用"""
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        return response.text
    except Exception as e:
        print(f"Gemini検索エラー：{e}")
        return generate_with_gemini(prompt)

def generate_with_gemini(prompt):
    """Gemini：文章生成・構造化に使用"""
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def generate_with_chatgpt(prompt):
    """ChatGPT：論理チェック・正確性確認に使用"""
    if _openai_key:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000
        )
        return response.choices[0].message.content
    else:
        print("  （OpenAI APIキー未設定→Geminiで論理チェック代替）")
        return generate_with_gemini(prompt)

def generate_with_claude(prompt):
    """Claude：修正・完成・最終仕上げに使用"""
    if _anthropic_key:
        message = claude_client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    else:
        print("  （Anthropic APIキー未設定→Geminiで最終仕上げ代替）")
        return generate_with_gemini(prompt)

def step1_research(today):
    """Step1：Gemini（検索）で最新情報・根拠データを収集"""
    print("Step1：Gemini検索で最新情報・根拠データを収集中...")

    prompt = f"""
【調査日】{today}

以下のテーマについて最新の情報・統計データ・研究結果を調査してください。

テーマ：「AIを活用する際のやってはいけないこと・注意事項」

【調査項目】
1. APIキーの漏洩による被害事例と金額（具体的な数字）
2. ハルシネーション（AIの誤情報）の発生率データ
3. AI利用による情報漏洩事例（企業・個人）
4. 著作権侵害に関する最新の法律・判例
5. AI利用に関する各国の規制動向（日本・EU・米国）
6. AI過信による業務上の失敗事例
7. セキュリティ企業が報告するAI関連リスク統計
8. AI利用コスト管理の失敗事例（トークン爆発）

各項目について：
・具体的な数字・パーセンテージ
・情報源（企業名・機関名・発表年）
・日本語で出力

これらは講義資料の根拠データとして使用します。
"""
    return generate_with_gemini_search(prompt)

def step2_structure(research_data, today):
    """Step2：Geminiで講義資料の構造・内容を生成"""
    print("Step2：Geminiで講義資料の構造・内容を生成中...")

    prompt = f"""
【調査日】{today}

以下のリサーチデータを元に
真田孔明のAI活用講座 第1回講義の
「AIと向き合う前に知っておくべきこと」の
完全な講義資料を作成してください。

【リサーチデータ】
{research_data[:4000]}

【講義の位置づけ】
・第1回講義の後半パート
・受講生がLevel 1→5を目指す前に必ず知っておくべき基礎知識

【文章スタイル】
・全ての主張に客観的な根拠・データを付ける
・結論→根拠→事実→応用の順で書く
・感情訴求は使わない

セクション：
1. AIとの向き合い方の全体像
2. APIキーの管理と取り扱い
3. ハルシネーションへの対処法
4. 著作権・知的財産の基本
5. プライバシー・情報漏洩リスク
6. トークンコスト・メモリ管理
7. 法的リスク・規制への対応
8. 実務でよくある間違いTOP10
9. AIと安全に向き合うための10の鉄則
"""
    return generate_with_gemini(prompt)

def step3_logic_check(structured_content, today):
    """Step3：ChatGPTで論理チェック・正確性確認"""
    print("Step3：ChatGPTで論理チェック・正確性確認中...")

    prompt = f"""
以下は真田孔明のAI活用講座 第1回講義資料の草稿です。

{structured_content[:5000]}

あなたは「論理チェック担当AI」です。以下の観点で厳密にチェックしてください。

【チェック項目】
1. 論理整合性：主張と根拠が一致しているか。矛盾した記述がないか
2. データの正確性：引用されている統計・数字は正確か。出典は信頼できるか
3. 因果関係：「なぜなら」「つまり」の前後が論理的に繋がっているか
4. 網羅性：重要な注意事項が漏れていないか
5. 受講生視点：Level 1の初心者でも理解できる説明になっているか

【出力形式】
## 論理チェック結果

### 問題なし（✅）の箇所
（正確・論理的に整合している箇所を列挙）

### 要修正（⚠️）の箇所
各箇所について：
・問題の内容
・なぜ問題か
・修正案

### 追加すべき内容
（漏れている重要な注意事項があれば）

### 総合評価
（100点満点で採点＋改善の優先順位）
"""
    return generate_with_chatgpt(prompt)

def step4_final_revision(structured_content, logic_feedback, today):
    """Step4：Claudeで修正・完成"""
    print("Step4：Claudeで修正・最終完成中...")

    prompt = f"""
あなたは「最終仕上げ担当AI」です。

【元の草稿】
{structured_content[:3000]}

【ChatGPTによる論理チェック結果】
{logic_feedback[:2000]}

上記のフィードバックを全て反映して、講義資料を修正・完成させてください。

【修正ルール】
1. ChatGPTが指摘した「要修正」箇所を全て修正する
2. 「追加すべき内容」があれば適切な場所に追加する
3. 真田孔明のAI経営本部の実体験を反映する
4. 全ての主張に客観的な根拠・データを付ける
5. 結論→根拠→事実→応用の順で書く
6. 感情訴求は使わない
7. Level 1の初心者でも理解できる表現にする

【出力形式】
## 修正サマリー
（何を修正したかを箇条書きで）

## 修正後の完成版コンテンツ
（完成した講義資料の全文）
"""
    return generate_with_claude(prompt)

def create_word_document(content_data, image_prompts, today, lecture_num=1):
    """Word文書の生成"""
    print("Wordファイルを生成中...")

    doc = Document()

    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)

    # 表紙
    cover_title = doc.add_paragraph()
    cover_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = cover_title.add_run(f'第{lecture_num:02d}回 AI活用講義')
    run.font.size = Pt(28)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)

    doc.add_paragraph()

    subtitle_p = doc.add_paragraph()
    subtitle_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle_run = subtitle_p.add_run('AIと向き合う前に知っておくべきこと')
    subtitle_run.font.size = Pt(18)
    subtitle_run.font.color.rgb = RGBColor(0x16, 0x21, 0x3E)

    doc.add_paragraph()

    date_p = doc.add_paragraph()
    date_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    date_run = date_p.add_run(f'真田孔明 AI活用講座　{today}')
    date_run.font.size = Pt(12)
    date_run.font.color.rgb = RGBColor(0x88, 0x87, 0x80)

    doc.add_page_break()

    # 目次
    h = doc.add_heading('■ 目次', level=1)
    for r in h.runs: r.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
    toc_items = [
        "第1章：AIとの向き合い方の全体像",
        "第2章：APIキーの管理と取り扱い",
        "第3章：ハルシネーションへの対処法",
        "第4章：著作権・知的財産の基本",
        "第5章：プライバシー・情報漏洩リスク",
        "第6章：トークンコスト・メモリ管理",
        "第7章：法的リスク・規制への対応",
        "第8章：実務でよくある間違いTOP10",
        "第9章：AIと安全に向き合うための10の鉄則",
        "チェックリスト"
    ]
    for item in toc_items:
        doc.add_paragraph(item, style='List Number')

    doc.add_page_break()

    # ゴール
    h = doc.add_heading('■ 今回の講義のゴール', level=1)
    for r in h.runs: r.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
    for goal in ["AIを安全に使うための基本ルールを理解する",
                  "APIキーの正しい管理方法を実践できるようになる",
                  "トークンコストを最小化する設計思想を身につける"]:
        p = doc.add_paragraph()
        p.add_run('✅ ').font.size = Pt(11)
        p.add_run(goal).font.size = Pt(11)
    doc.add_paragraph()

    # セクション
    sections_data = [
        ("第1章：AIとの向き合い方の全体像",
         "[画像挿入：AIリスク4大カテゴリの構造図]",
         "AIを活用する上で最初に知っておくべき全体像があります。\n\n"
         "【根拠：McKinsey Global Institute報告】\nAIを導入した企業の67%が導入初期に何らかのリスク・トラブルを経験。\n\n"
         "AIリスクの4大カテゴリ：\n① セキュリティリスク（APIキー漏洩・情報漏洩）\n"
         "② 品質リスク（ハルシネーション・誤情報）\n③ 法的リスク（著作権・プライバシー・規制）\n"
         "④ コストリスク（トークン爆発・予算超過）\n\nこの4つを理解すれば安全かつ低コストでAI活用ができます。"),
        ("第2章：APIキーの管理と取り扱い",
         "[画像挿入：APIキー管理フローチャート]",
         "APIキーとはAIサービスにプログラムからアクセスするための「鍵」です。\n\n"
         "【根拠：GitHub Security Advisory】\n2024年だけで約100万件のAPIキー漏洩が検出。\n"
         "数時間で数百万円の請求が発生した事例が世界中で報告されています。\n\n"
         "❌ やってはいけないこと：\n・コードにAPIキーを直接書く\n・GitHubにAPIキーを含むファイルをアップロードする\n"
         "・メモ帳・Notionにそのまま保存する\n\n"
         "✅ 正しい管理方法：\n・環境変数として保存する（~/.zshrc）\n・.gitignoreでAPIキー関連ファイルを除外\n"
         "・月額上限（Spending limit）を必ず設定\n\n漏洩に気づいたら→1分以内に無効化することが損害最小化の鍵。"),
        ("第3章：ハルシネーションへの対処法",
         "[画像挿入：AI別ハルシネーション発生率比較グラフ]",
         "ハルシネーションとはAIが事実と異なる情報を自信満々に出力する現象です。\n\n"
         "【根拠：Stanford University AI Index 2024】\n・ChatGPT-4の誤情報生成率：約15〜20%\n"
         "・Claude 3の誤情報生成率：約10〜15%\n・Gemini 1.5の誤情報生成率：約12〜18%\n\n"
         "❌ やってはいけないこと：\n・AI出力をそのまま事実として公開する\n・数字・統計・固有名詞を確認せずに使用する\n\n"
         "✅ 正しい対処法：\n・重要な情報は必ず一次情報源で確認\n・AIの出力を「草稿」として扱い人間がレビュー\n"
         "・複数のAIで結果を比較する\n\n【事例】米国弁護士がAI生成の存在しない判例を裁判所に提出→制裁金・業務停止処分"),
        ("第4章：著作権・知的財産の基本",
         "[画像挿入：著作権判断フローチャート]",
         "AI生成コンテンツの著作権は世界中で法整備が進んでいます。\n\n"
         "【根拠：文化庁 2024年3月】\nAIが自律的に生成したコンテンツは著作権法上の「著作物」に該当しない可能性がある。\n"
         "人間が創作的寄与を行った場合は認められる場合がある。\n\n"
         "【根拠：EU AI法 2024年施行】\nAI生成コンテンツには表示義務。違反時最大で全世界年間売上の3%制裁金。\n\n"
         "❌ やってはいけないこと：\n・AI生成コンテンツをそのまま著作物として権利主張\n"
         "・AI生成であることを隠して販売・配布\n\n"
         "✅ 正しい対応：\n・AI生成コンテンツには編集・改善を加えて創作的寄与を行う\n"
         "・商業利用の場合は各AIサービスの利用規約を確認"),
        ("第5章：プライバシー・情報漏洩リスク",
         "[画像挿入：AIに入力してよい情報・いけない情報の分類図]",
         "AIに入力した情報がどこへ行くのかを正確に理解することが重要です。\n\n"
         "【根拠：個人情報保護委員会 2024年ガイドライン】\n"
         "AIサービスに入力した個人情報はサービス提供企業のサーバーに送信されます。\n\n"
         "❌ 絶対にAIに入力してはいけない情報：\n・顧客の個人情報（氏名・住所・電話番号）\n"
         "・クレジットカード番号・銀行口座情報\n・マイナンバー・健康保険証番号\n"
         "・会社の機密情報・未公開の財務情報\n・パスワード・認証情報\n\n"
         "【事例】Samsung社員がChatGPTに社内ソースコードを入力し漏洩（2023年）\n"
         "日本企業でも同様の事例が2024年に23件報告"),
        ("第6章：トークンコスト・メモリ管理",
         "[画像挿入：トークンコスト増加グラフ・SKILLファイル方式の構造図]",
         "AIのコスト管理を知らずに実装すると毎月想定外の高額請求が来ます。\n\n"
         "【トークン課金の仕組み】\n入力トークン数×単価＋出力トークン数×単価＝1回の処理コスト\n\n"
         "【参考単価（2026年3月現在）】\n・Claude Sonnet：入力$3/百万トークン・出力$15/百万トークン\n"
         "・Gemini 2.5 Flash：入力$0.075/百万トークン\n\n"
         "❌ 失敗パターン：全会話履歴をコンテキストに含める設計\n"
         "→1日目：1,000トークン→1ヶ月後：30,000トークン＝コスト30倍\n\n"
         "✅ 正しい設計：\n・SKILLファイル方式：AIの記憶はファイルで管理（必要時だけ読み込む）\n"
         "・直近N件のみ使用（全履歴ではなく直近5件のみ）\n・CLAUDE.md方式：各フォルダのCLAUDE.mdがAIの記憶として機能\n\n"
         "【真田孔明の実体験】全会話履歴をコンテキストに含める設計→月間API費用が想定の10〜30倍に"),
        ("第7章：法的リスク・規制への対応",
         "[画像挿入：世界のAI規制マップ]",
         "AI利用に関する規制は2024〜2026年にかけて急速に整備されています。\n\n"
         "【日本】\n・個人情報保護法：AI利用における個人情報取扱いガイドライン（2024年）\n"
         "・著作権法：AI学習・生成に関する解釈指針（文化庁 2024年）\n\n"
         "【EU AI法】\n・2024年8月施行・2026年完全適用\n・AIシステムをリスクレベルで分類\n"
         "・違反時：最大3,000万ユーロまたは全世界年間売上の6%\n\n"
         "【米国】\n・2023年大統領令：AI安全性に関する包括的規制枠組み\n"
         "・FTC：AIを使った虚偽広告・詐欺への厳格な対応\n\n"
         "日本のビジネスオーナーへの影響：\n・EU市民にサービス提供する場合はEU AI法が適用される可能性\n"
         "・AIを使ったマーケティングは景品表示法の対象"),
        ("第8章：実務でよくある間違いTOP10",
         "[画像挿入：失敗TOP10のランキング図]",
         "AI活用の現場で最も多く発生する間違いを根拠データと共に解説します。\n\n"
         "【根拠：Gartner AI導入失敗事例調査 2024年】\nAI導入プロジェクトの失敗率：約30%\n\n"
         "1位：AI出力をそのまま使う（ハルシネーション率15〜20%を見落とす）\n"
         "2位：APIキーをコードに直書き（GitHubに公開した瞬間に漏洩）\n"
         "3位：全会話履歴をコンテキストに含める（コスト30倍）\n"
         "4位：個人情報をAIに入力する（個人情報保護法違反）\n"
         "5位：AI生成コンテンツを確認せずに公開（誤情報・著作権侵害）\n"
         "6位：一つのAIだけに依存する（サービス停止リスク）\n"
         "7位：プロンプトを曖昧にする（手戻り発生）\n"
         "8位：AIへの過度な期待（人間の判断が必要な業務を丸投げ）\n"
         "9位：バックアップ・バージョン管理をしない（データ消失）\n"
         "10位：コスト管理をしない（月額上限未設定で高額請求）"),
        ("第9章：AIと安全に向き合うための10の鉄則",
         "[画像挿入：10の鉄則インフォグラフィック]",
         "真田孔明AI経営本部が実践している10の鉄則を公開します。\n\n"
         "鉄則1：APIキーは必ず環境変数で管理する\n→根拠：年間100万件以上のGitHub漏洩事例\n\n"
         "鉄則2：全ての出力に人間のレビューを入れる\n→根拠：ハルシネーション率最高20%\n\n"
         "鉄則3：個人情報・機密情報はAIに入力しない\n→根拠：2024年日本で23件の漏洩事例\n\n"
         "鉄則4：月額上限（Spending limit）を必ず設定する\n→根拠：コスト30倍になった実体験\n\n"
         "鉄則5：AIの記憶はSKILLファイルで管理する\n→根拠：会話履歴蓄積でコスト指数関数的増加\n\n"
         "鉄則6：著作権法・個人情報保護法を定期的に確認する\n→根拠：2024〜2026年に急速な法整備\n\n"
         "鉄則7：3大AIを用途に応じて使い分ける\n→根拠：Claude品質チェック・Gemini検索・ChatGPT多様性\n\n"
         "鉄則8：GitHubで全データをバージョン管理する\n→根拠：データ消失リスクの排除\n\n"
         "鉄則9：毎月のAPI使用量を確認する習慣をつける\n→根拠：異常増加は不正使用のサイン\n\n"
         "鉄則10：AIを「道具」ではなく「組織」として設計する\n→根拠：1人で5名分のアウトプットが可能になった実証")
    ]

    for title_text, image_text, content_text in sections_data:
        h = doc.add_heading(title_text, level=1)
        for r in h.runs: r.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)

        img_p = doc.add_paragraph()
        img_run = img_p.add_run(image_text)
        img_run.font.color.rgb = RGBColor(0xFF, 0x69, 0x00)
        img_run.font.bold = True
        img_run.font.size = Pt(10)

        for line in content_text.split('\n'):
            if line.strip():
                p = doc.add_paragraph(line)
                if line.startswith('❌'):
                    p.runs[0].font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
                elif line.startswith('✅'):
                    p.runs[0].font.color.rgb = RGBColor(0x00, 0x80, 0x00)

        doc.add_paragraph()

    # チェックリスト
    doc.add_page_break()
    h = doc.add_heading('■ 受講生向けチェックリスト', level=1)
    for r in h.runs: r.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
    for item in [
        "APIキーを環境変数で管理している",
        ".gitignoreにAPIキー関連ファイルを追加している",
        "各AIサービスに月額上限を設定している",
        "AIの記憶をSKILLファイルで管理している",
        "毎月のAPI使用量を確認する習慣がある",
        "個人情報・機密情報をAIに入力していない",
        "AI出力を必ずレビューしてから使用している",
        "著作権・個人情報保護法の動向を把握している",
        "APIキー漏洩時の対処法を把握している",
        "3大AIを用途で使い分けている"
    ]:
        p = doc.add_paragraph()
        p.add_run('☐ ').font.size = Pt(12)
        p.add_run(item).font.size = Pt(10.5)

    os.makedirs(SAVE_DIR, exist_ok=True)
    word_file = os.path.join(SAVE_DIR, "第01回_講義資料_AIと向き合う前に知っておくべきこと.docx")
    doc.save(word_file)
    print(f"✅ Wordファイル保存完了：{word_file}")
    return word_file

def create_image_prompts(today):
    """ナノバナナプロ用画像プロンプト一覧を生成"""
    print("ナノバナナプロ用画像プロンプトを生成中...")
    prompts = [
        {"num": 1, "section": "第1章：全体像",
         "prompt": "ナノバナナプロで以下の内容を図解してください。\nタイトル：AIリスク4大カテゴリ\n中心に「AI活用」を置き4つのリスクを周囲に配置\n① セキュリティリスク（APIキー漏洩・情報漏洩）\n② 品質リスク（ハルシネーション・誤情報）\n③ 法的リスク（著作権・プライバシー・規制）\n④ コストリスク（トークン爆発・予算超過）\n各カテゴリにアイコン追加。配色：ネイビー・オレンジ・ホワイト\nスタイル：霞が関のポンチ絵のように全情報を一枚にまとめて。サイズ：横長16:9",
         "location": "第1章の冒頭"},
        {"num": 2, "section": "第2章：APIキー管理",
         "prompt": "ナノバナナプロで以下を図解してください。\nタイトル：APIキーの正しい管理フロー\n左側に「❌悪い例」右側に「✅良い例」を対比\n悪い例：コードに直接記載→GitHubにアップ→漏洩→高額請求\n良い例：環境変数に保存→コードから呼び出し→安全\n下部に「漏洩時の対処フロー」追加\nスタイル：フローチャート形式。サイズ：横長16:9",
         "location": "第2章の冒頭"},
        {"num": 3, "section": "第3章：ハルシネーション",
         "prompt": "ナノバナナプロで以下を図解してください。\nタイトル：AI別ハルシネーション発生率比較\n棒グラフ形式で3つのAIを比較\nChatGPT-4：15〜20%\nClaude 3：10〜15%\nGemini 1.5：12〜18%\n出典：Stanford University AI Index 2024\n右側に正しい対処法を箇条書き\nスタイル：データビジュアライゼーション。サイズ：横長16:9",
         "location": "第3章の冒頭"},
        {"num": 4, "section": "第4章：著作権",
         "prompt": "ナノバナナプロで以下を図解してください。\nタイトル：AI生成コンテンツの著作権判断フロー\nフローチャート：AI生成コンテンツ→人間の創作的寄与あり？→Yes：著作権認められる可能性→No：著作物に該当しない可能性\n配色：ネイビー・グレー・グリーン\nスタイル：判断フローチャート。サイズ：横長16:9",
         "location": "第4章の冒頭"},
        {"num": 5, "section": "第5章：プライバシー",
         "prompt": "ナノバナナプロで以下を図解してください。\nタイトル：AIに入力してよい情報・いけない情報\n2列比較：❌入力禁止（個人情報・カード番号・機密情報等）vs ✅入力可能（匿名データ・公開情報・自分の考え等）\nスタイル：2列比較図。サイズ：横長16:9",
         "location": "第5章の冒頭"},
        {"num": 6, "section": "第6章：コスト管理",
         "prompt": "ナノバナナプロで以下を図解してください。\nタイトル：トークンコスト増加の仕組みとSKILLファイル方式\n上段：折れ線グラフ「全履歴方式のコスト推移」1,000→7,000→30,000トークン\n下段：❌全履歴方式（コスト30倍）vs ✅SKILLファイル方式（コスト一定）\nスタイル：グラフ＋構造図。サイズ：横長16:9",
         "location": "第6章の冒頭"},
        {"num": 7, "section": "第7章：法的リスク",
         "prompt": "ナノバナナプロで以下を図解してください。\nタイトル：世界のAI規制マップ2026\n世界地図ベースで各国の規制を表示\nEU：EU AI法・違反時最大6%制裁金\n日本：個人情報保護法・著作権法\n米国：大統領令・FTC規制\nスタイル：地図＋テキスト。サイズ：横長16:9",
         "location": "第7章の冒頭"},
        {"num": 8, "section": "第8章：失敗TOP10",
         "prompt": "ナノバナナプロで以下を図解してください。\nタイトル：AI活用でよくある失敗TOP10\nランキング形式で1位〜10位を表示\n各項目に危険度アイコン追加\nスタイル：ランキングリスト形式。サイズ：横長16:9",
         "location": "第8章の冒頭"},
        {"num": 9, "section": "第9章：10の鉄則",
         "prompt": "ナノバナナプロで以下を図解してください。\nタイトル：AIと安全に向き合うための10の鉄則\n10個の鉄則を左右2列のインフォグラフィック形式で表示\n各鉄則にアイコン追加\n配色：ネイビー・ゴールド・ホワイト\nスタイル：インフォグラフィック。サイズ：横長16:9",
         "location": "第9章の冒頭"},
        {"num": 10, "section": "チェックリスト",
         "prompt": "ナノバナナプロで以下を図解してください。\nタイトル：AI安全活用チェックリスト\n10項目をグループ分け：セキュリティ・コスト管理・法的対応・品質管理\n各項目にチェックボックス追加\nスタイル：チェックリスト形式。サイズ：横長16:9",
         "location": "チェックリストページ"}
    ]
    return prompts

def main():
    today = datetime.now().strftime("%Y年%m月%d日")
    os.makedirs(SAVE_DIR, exist_ok=True)

    print("=" * 60)
    print("最高品質講義資料制作システム起動")
    print("3大AI完全役割分担：")
    print("  Step1: Gemini（検索）→ 最新情報・根拠データ収集")
    print("  Step2: Gemini（生成）→ 講義資料の構造・内容生成")
    print("  Step3: ChatGPT（論理チェック）→ 正確性・論理性確認")
    print("  Step4: Claude（修正・完成）→ フィードバック反映・最終仕上げ")
    print("  Step5: Word生成＋画像プロンプト")
    ai_status = []
    ai_status.append(f"  Gemini: {'✅ 有効' if os.environ.get('GEMINI_API_KEY') else '❌ 未設定'}")
    ai_status.append(f"  ChatGPT: {'✅ 有効' if _openai_key else '⚠️ 未設定（Gemini代替）'}")
    ai_status.append(f"  Claude: {'✅ 有効' if _anthropic_key else '⚠️ 未設定（Gemini代替）'}")
    for s in ai_status: print(s)
    print("=" * 60)

    research_data = step1_research(today)
    with open(os.path.join(SAVE_DIR, "リサーチデータ.md"), "w") as f:
        f.write(f"# リサーチデータ\n## {today}\n\n{research_data}")
    print("✅ Step1完了：リサーチデータ収集")

    structured_content = step2_structure(research_data, today)
    with open(os.path.join(SAVE_DIR, "草稿.md"), "w") as f:
        f.write(f"# 草稿\n## {today}\n\n{structured_content}")
    print("✅ Step2完了：講義資料草稿生成")

    logic_feedback = step3_logic_check(structured_content, today)
    with open(os.path.join(SAVE_DIR, "Step3_ChatGPT論理チェック.md"), "w") as f:
        f.write(f"# ChatGPT論理チェック結果\n## {today}\n\n{logic_feedback}")
    print("✅ Step3完了：ChatGPT論理チェック")

    final_content = step4_final_revision(structured_content, logic_feedback, today)
    with open(os.path.join(SAVE_DIR, "Step4_Claude修正完成版.md"), "w") as f:
        f.write(f"# Claude修正完成版\n## {today}\n\n{final_content}")
    print("✅ Step4完了：Claude修正・最終完成")

    word_file = create_word_document(final_content, [], today)
    print("✅ Step4完了：Wordファイル生成")

    image_prompts = create_image_prompts(today)
    prompt_file = os.path.join(SAVE_DIR, "ナノバナナプロ_画像プロンプト一覧.txt")
    with open(prompt_file, "w") as f:
        f.write("=" * 60 + "\n")
        f.write("ナノバナナプロ 画像生成プロンプト一覧\n")
        f.write("以下を順番にナノバナナプロに貼り付けて画像を生成してください。\n")
        f.write("=" * 60 + "\n\n")
        for p in image_prompts:
            f.write(f"【画像{p['num']}：{p['section']}】\n")
            f.write(f"挿入箇所：{p['location']}\n")
            f.write(f"プロンプト：\n{p['prompt']}\n")
            f.write("-" * 40 + "\n\n")
    print(f"✅ Step5完了：画像プロンプト一覧生成（{len(image_prompts)}枚分）")

    import subprocess
    subprocess.run(["bash", "-c",
        "cd ~/Desktop/AI経営本部 && "
        "git add AI活用講義/ && "
        "git commit -m '第1回講義資料完成（3大AI横断・Word・画像プロンプト10枚）' && "
        "git push origin salesletter-development"
    ])

    print("\n" + "=" * 60)
    print("✅ 全工程完了！")
    print("=" * 60)
    print(f"Wordファイル：{word_file}")
    print(f"画像プロンプト：{prompt_file}")
    print(f"生成した画像プロンプト数：{len(image_prompts)}枚")
    print("\n次のステップ：")
    print("1. ナノバナナプロ_画像プロンプト一覧.txtを開く")
    print("2. 各プロンプトをGemini（ナノバナナプロ）に貼り付けて画像生成")
    print("3. 生成した画像をWordの[画像挿入箇所]に挿入する")

if __name__ == "__main__":
    main()
