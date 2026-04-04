#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINEステップメール原稿(.txt)を読み込み専用で4倍展開してメルマガ生成
P-01から順番にT-10まで自動進行
"""

import os
import json
import glob
from datetime import datetime
import google.generativeai as genai

# 設定
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# パス設定
BASE_DIR = os.path.expanduser("~/Desktop/AI経営本部")
LINE_DIR = f"{BASE_DIR}/レベルファイブAI経営マスタリー/LINEステップメール/QUEST1/本文"
OUTPUT_DIR = f"{BASE_DIR}/レベルファイブAI経営マスタリー/メルマガ原稿"
COUNTER_FILE = f"{BASE_DIR}/API連携/Gemini/merumaga_line_progress.json"

# 読み込み順序（全105話）
PHASES = [
    ("P", 15),  # プロローグ
    ("Q", 10),  # 絞り込み
    ("U", 20),  # 共感
    ("E", 30),  # 教育
    ("S", 20),  # 刺激
    ("T", 10),  # 行動促進
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
4. 具体例・エピソード・深掘り・感情描写で自然に膨らませる
5. テーマ: レベルファイブAI経営マスタリー
6. 文体: 一人称「僕」・です/ます調・読者を「あなた」と呼ぶ
7. 真田孔明の実体験を織り交ぜる
8. 成功シンドロームOSの言語化禁止・架空事例禁止・煽り表現禁止

【真田孔明プロフィール（必須）】
・1976年生まれ・2004年からメルマガ配信20年以上
・海外・日本複数法人の経営
・韓国焼肉レストラン運営
・米国株投資コミュニティ「北の株式投資大学」管理
・NVIDIA早期保有→金融資産20億超
・メンター: マスターヒロ（大富豪投資家）
・エンジニアゼロで48時間でAI経営本部構築

【重要設定：エンジニアのビジネスパートナーについて（厳守）】
・2026年2月に50代のビジネスパートナーが急逝
・このパートナーは「プロジェクトの一部、技術面をお願いしていただけ」
・「全てのビジネスに関わっていたわけではない」
・気心知れたエンジニアにお願いできなくなった状況が、AIの力で補おうと考えたキッカケ
・この話をする際は、この設定を間違えないこと

【文字数目標】
・序論: 900〜1,000文字
・本論1: 900〜1,000文字
・本論2: 900〜1,000文字
・結論: 900〜1,000文字
・合計: 3,600〜4,000文字

【出力フォーマット】
序論:
（ここに900〜1,000文字の序論を展開）

本論1:
（ここに900〜1,000文字の本論1を展開）

本論2:
（ここに900〜1,000文字の本論2を展開）

結論:
（ここに900〜1,000文字の結論を展開）

━━━━━━━━━━━━━━
             真田孔明
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
        f.write(f"# メルマガ原稿 #{counter['total_count']+1}\n")
        f.write(f"# 元ネタ: {file_code} ({os.path.basename(current_file)})\n")
        f.write(f"# 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
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
