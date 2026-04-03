#!/usr/bin/env python3
"""LINEステップメール原稿を基にメルマガを4倍展開生成（Gemini版）"""

import os, json, re
from datetime import datetime

BASE_DIR = os.path.expanduser("~/Desktop/AI経営本部")
LINE_DIR = "%s/レベルファイブAI経営マスタリー/LINEステップメール" % BASE_DIR
OUTPUT_DIR = "%s/集客販売/メルマガ原稿" % BASE_DIR
COUNTER_FILE = "%s/API連携/Gemini/merumaga_counter.json" % BASE_DIR

LINE_FILES = [
    ("プロローグ_コアストーリー15話_v2.md", 15),
    ("QUEST1_Q絞り込み_10話.md", 10),
    ("QUEST1_U共感_20話_完全版.md", 20),
    ("QUEST1_S刺激_20話_完全版.md", 20),
    ("QUEST1_E教育_30話_設計図.md", 30),
    ("QUEST1_T行動促進_10話_完全版.md", 10),
]

def load_counter():
    if os.path.exists(COUNTER_FILE):
        return json.load(open(COUNTER_FILE))
    return {"file_index": 0, "talk_number": 1, "total_count": 0}

def save_counter(c):
    with open(COUNTER_FILE, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)

def extract_talk(filepath, talk_number):
    if not os.path.exists(filepath):
        return None
    content = open(filepath, encoding="utf-8").read()
    patterns = [
        r"##\s*(?:プロローグ)?第%d話.*?\n(.*?)(?=##\s*(?:プロローグ)?第\d+話|---\s*$|\Z)" % talk_number,
        r"##\s*[A-Z]第%d話.*?\n(.*?)(?=##\s*[A-Z]第\d+話|---\s*$|\Z)" % talk_number,
        r"\*\*[A-Z]第%d話.*?\*\*\n(.*?)(?=\*\*[A-Z]第\d+話|\Z)" % talk_number,
    ]
    for p in patterns:
        m = re.search(p, content, re.DOTALL)
        if m:
            return m.group(1).strip()
    return None

def expand_to_merumaga(line_content, talk_info):
    import google.genai as genai
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
    prompt = """あなたは真田孔明のメルマガライターです。
以下のLINEステップメール原稿(900-1000字)をメルマガ用に4倍展開して3600-4000字にしてください。

【元ネタLINE原稿】
%s

【展開ルール】
1. 構成: 序論900-1000字→本論①900-1000字→本論②900-1000字→結論900-1000字
2. テーマ: レベルファイブAI経営マスタリー
3. LINE原稿の核心メッセージを維持しつつ具体例・エピソード・深掘りで展開
4. 文体: 一人称「僕」・です/ます調・「あなた」と呼びかけ
5. 真田孔明の実体験・NVIDIA投資・マスターヒロの教えなどを織り交ぜる
6. 成功シンドロームOSの言語化禁止・架空事例禁止
7. 最初の行に「件名：」としてメルマガ全体のタイトルを書く

【出力フォーマット】
件名：（読者が開封したくなるタイトル）

◯[序論タイトル]
(900-1000字)

◯[本論①タイトル]
(900-1000字)

◯[本論②タイトル]
(900-1000字)

◯[結論タイトル]
(900-1000字)

　　　　　　　　　　　　真田孔明
""" % line_content

    r = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return r.text

def main():
    counter = load_counter()
    if counter["file_index"] >= len(LINE_FILES):
        print("全話完了。カウンターをリセットします")
        counter = {"file_index": 0, "talk_number": 1, "total_count": counter["total_count"]}
        save_counter(counter)

    current_file, max_talks = LINE_FILES[counter["file_index"]]
    current_talk = counter["talk_number"]
    filepath = "%s/%s" % (LINE_DIR, current_file)

    print("=== メルマガ生成（Gemini版）===")
    print("  元ネタ: %s 第%d話" % (current_file, current_talk))

    line_content = extract_talk(filepath, current_talk)
    if not line_content:
        print("  ❌ 話数抽出失敗: %s 第%d話" % (current_file, current_talk))
        return

    print("  ✅ LINE原稿読み込み完了（%d字）" % len(line_content))
    print("  ✍️ Geminiで4倍展開中...")

    merumaga = expand_to_merumaga(line_content, "%s 第%d話" % (current_file, current_talk))
    print("  ✅ メルマガ生成完了（%d字）" % len(merumaga))

    today = datetime.now().strftime("%Y%m%d")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_file = "%s/%s_メルマガ_%03d.txt" % (OUTPUT_DIR, today, counter["total_count"] + 1)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("# メルマガ原稿 #%d\n" % (counter["total_count"] + 1))
        f.write("# 元ネタ: %s 第%d話\n" % (current_file, current_talk))
        f.write("# 生成日時: %s\n\n" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        f.write(merumaga)
    print("  ✅ 保存: %s" % os.path.basename(out_file))

    counter["talk_number"] += 1
    counter["total_count"] += 1
    if counter["talk_number"] > max_talks:
        counter["file_index"] += 1
        counter["talk_number"] = 1
    save_counter(counter)
    print("  📍 次回: ファイル%d/%d 第%d話" % (counter["file_index"] + 1, len(LINE_FILES), counter["talk_number"]))

if __name__ == "__main__":
    main()
