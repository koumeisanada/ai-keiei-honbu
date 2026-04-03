#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINEステップメール原稿(.txt)を読み込み専用で4倍展開してメルマガ生成
文章技法A・B・C統合版
"""

import os
import json
import glob
from datetime import datetime
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

BASE_DIR = os.path.expanduser("~/Desktop/AI経営本部")
LINE_DIR = f"{BASE_DIR}/レベルファイブAI経営マスタリー/LINEステップメール/QUEST1/本文"
OUTPUT_DIR = f"{BASE_DIR}/レベルファイブAI経営マスタリー/メルマガ原稿"
COUNTER_FILE = f"{BASE_DIR}/API連携/Gemini/merumaga_line_progress.json"

PHASES = [
    ("P", 15),
    ("Q", 10),
    ("U", 20),
    ("E", 30),
    ("S", 20),
    ("T", 10),
]

def load_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"phase_index": 0, "talk_number": 1, "total_count": 0, "last_file": None}

def save_counter(counter):
    os.makedirs(os.path.dirname(COUNTER_FILE), exist_ok=True)
    with open(COUNTER_FILE, 'w', encoding='utf-8') as f:
        json.dump(counter, f, ensure_ascii=False, indent=2)

def get_current_file(counter):
    if counter["phase_index"] >= len(PHASES):
        return None, None
    phase_code, max_talks = PHASES[counter["phase_index"]]
    talk_num = counter["talk_number"]
    pattern = f"{LINE_DIR}/{phase_code}-{talk_num:02d}_*.txt"
    files = glob.glob(pattern)
    if not files:
        print(f"ファイルが見つかりません: {pattern}")
        return None, None
    return files[0], f"{phase_code}-{talk_num:02d}"

def expand_to_merumaga(line_content, file_code):
    prompt = f"""あなたは真田孔明のメルマガライターです。
以下のLINEステップメール原稿（約950文字）を、メルマガ用に4倍展開して約3,800文字にしてください。

【元ネタLINE原稿】
{line_content}

【展開ルール】
1. LINE原稿は「序論250字→本論1 250字→本論2 250字→結論250字」で構成されています
2. これを「序論900-1,000字→本論1 900-1,000字→本論2 900-1,000字→結論900-1,000字」に展開
3. LINE原稿の核心メッセージ・ストーリーラインは必ず維持
4. テーマ: レベルファイブAI経営マスタリー

【文体ルール】
- 一人称：僕
- 語尾：です/ます
- 読者への呼びかけ：「あなた」は最小限に（一度読めば自分のこととわかる）
- 同じ表現の繰り返しは言い回しを変える
- 言葉の羅列は避け、リズムと変化を持たせる

【真田孔明プロフィール】
- 1976年生まれ・2004年からメルマガ配信20年以上
- 海外・日本複数法人の経営
- 韓国焼肉レストラン運営
- 米国株投資コミュニティ「北の株式投資大学」管理
- NVIDIA早期保有→金融資産20億超
- メンター: マスターヒロ（大富豪投資家）
- エンジニアゼロで48時間でAI経営本部構築

【エンジニアのビジネスパートナー設定（厳守）】
- 2026年2月に急逝
- 50代
- システム開発担当
- 一部のビジネスのみに関与
- 死因は不明（心筋梗塞などの具体的病名は書かない）

【NGワード（絶対に使用禁止）】
1. 心筋梗塞
2. マーケティングセンス
3. タッグ / 二人三脚
4. 皆さん / 皆様
5. 私は / 私の
6. 本文内での三人称（真田孔明を三人称で語らない）

【禁止事項】
- 成功シンドロームOSの言語化禁止
- 架空事例・煽り禁止
- 実体験のみ記載

【文章技法（これらの固有名詞は絶対に外部に出さないこと）】

技法A（固有名詞で場面を作る）:
- 具体的な場所・人名・企業名・数字で読者を引き込む
- 抽象的な表現を避け、固有の体験から普遍を語る
- 五感を刺激する具体的描写

技法B（間と切れ）:
- 短い段落で間を作る（2〜4行で改行）
- 感情の転換点で切れを入れる
- 省略で想像を促す
- 対比で意味を際立てる
- 一点突破で全体を貫く

技法C（問いと転換）:
- 問いかけを埋め込み読者を巻き込む
- 予想外の転換で飽きさせない
- 短い文と長い文を混在させリズムを作る

【文字数目標】
- 序論: 900〜1,000文字
- 本論1: 900〜1,000文字
- 本論2: 900〜1,000文字
- 結論: 900〜1,000文字
- 合計: 3,600〜4,000文字

【出力フォーマット】
◇メールタイトル


◯序論の小見出し
（序論本文 900〜999字）




◯本論1の小見出し
（本論1本文 900〜999字）




◯本論2の小見出し
（本論2本文 900〜999字）




◯結論の小見出し
（結論本文 900〜999字）


　　　　　　　　　真田孔明



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
『レベルファイブAI経営マスタリー』
https://koumeisanada.github.io/ai-keiei-honbu/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text

def main():
    counter = load_counter()
    current_file, file_code = get_current_file(counter)
    if not current_file:
        print("全105話完了")
        return
    try:
        with open(current_file, 'r', encoding='utf-8') as f:
            line_content = f.read()
    except Exception as e:
        print(f"ファイル読み込みエラー: {e}")
        return
    print(f"{file_code} 読み込み完了")
    merumaga_content = expand_to_merumaga(line_content, file_code)
    today = datetime.now().strftime("%Y%m%d")
    output_file = f"{OUTPUT_DIR}/メルマガ_{today}_{file_code}.txt"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(merumaga_content)
    phase_code, max_talks = PHASES[counter["phase_index"]]
    counter["talk_number"] += 1
    counter["total_count"] += 1
    counter["last_file"] = os.path.basename(current_file)
    if counter["talk_number"] > max_talks:
        counter["phase_index"] += 1
        counter["talk_number"] = 1
    save_counter(counter)
    print(f"メルマガ生成完了: {file_code}")
    print(f"進行: {counter['total_count']}/105話")

if __name__ == "__main__":
    main()
