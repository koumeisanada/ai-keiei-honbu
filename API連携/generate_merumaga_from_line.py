#!/usr/bin/env python3
"""LINEステップメール連動型 メルマガ自動生成スクリプト"""
import os, json, subprocess, time
from datetime import datetime

BASE = os.path.expanduser("~/Desktop/AI経営本部")
LINE_DIR = os.path.join(BASE, "レベルファイブAI経営マスタリー/LINEステップメール/QUEST1/本文")
OUTPUT_DIR = os.path.join(BASE, "レベルファイブAI経営マスタリー/メルマガ原稿")
API_DIR = os.path.join(BASE, "API連携")
os.makedirs(OUTPUT_DIR, exist_ok=True)
PROGRESS_FILE = os.path.join(API_DIR, "merumaga_line_progress.json")

PHASE_ORDER = [
    {"phase": "P", "count": 15}, {"phase": "Q", "count": 10},
    {"phase": "U", "count": 20}, {"phase": "E", "count": 30},
    {"phase": "S", "count": 20}, {"phase": "T", "count": 10},
]

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        return json.load(open(PROGRESS_FILE))
    return {"phase": "P", "number": 1, "total_sent": 0}

def save_progress(p):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False, indent=2)

def next_progress(cur):
    phase, number = cur["phase"], cur["number"]
    info = next(p for p in PHASE_ORDER if p["phase"] == phase)
    if number < info["count"]:
        return {"phase": phase, "number": number + 1, "total_sent": cur["total_sent"] + 1}
    idx = next(i for i, p in enumerate(PHASE_ORDER) if p["phase"] == phase)
    if idx < len(PHASE_ORDER) - 1:
        return {"phase": PHASE_ORDER[idx + 1]["phase"], "number": 1, "total_sent": cur["total_sent"] + 1}
    return {"phase": "P", "number": 1, "total_sent": cur["total_sent"] + 1}

def load_line_content(phase, number):
    for ext in [".md", ".txt"]:
        # ファイル名パターンを検索
        prefix = "%s-%02d" % (phase, number)
        for f in os.listdir(LINE_DIR):
            if f.startswith(prefix) and f.endswith(ext):
                return open(os.path.join(LINE_DIR, f), encoding="utf-8").read()
    return None

def get_latest_ai_news():
    try:
        import google.genai as genai
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
        r = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="直近7日以内のAI業界の最重要ニュースを3つ。Claude・ChatGPT・Gemini関連優先。各100字以内。出典付き。"
        )
        return r.text
    except Exception as e:
        return "AI最新情報取得エラー：%s" % e

def generate_merumaga(line_content, phase, number, ai_news):
    import anthropic
    labels = {"P": "プロローグ", "Q": "絞り込み", "U": "共感", "E": "教育", "S": "刺激", "T": "行動促進"}
    client = anthropic.Anthropic()
    prompt = """以下のLINEステップメール %s-%02d（%s）を元に、メルマガ（4セクション×各1,000字＝合計4,000字）を執筆してください。

【LINE原文】
%s

【今週のAI最新情報（地合いとして自然に盛り込む）】
%s

【執筆ルール】
・LINEの内容を4倍に展開する
・AI最新情報は「地合い」として自然に1〜2回触れる
・一人称：僕 / です・ます調 / 「あなた」への手紙
・「みなさん」禁止 / 架空事例禁止 / 時間表現禁止
・「成功シンドロームOS」という言葉を出さない
・段落：2〜4行で改行
・見出し：◯タイトル
・末尾署名：全角スペース12個＋真田孔明

【4セクション構成】
◯[序論タイトル]（約1,000字）
◯[本論①タイトル]（約1,000字）
◯[本論②タイトル]（約1,000字）
◯[結論・CTAタイトル]（約1,000字）
""" % (phase, number, labels.get(phase, phase), line_content, ai_news)

    response = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=6000,
        system="あなたは真田孔明のメルマガ専任ライターです。村上春樹的な感覚描写・俳句的な余白・Seth Godin的な短段落を自然に使いますが技法の存在を気づかせません。",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    today = datetime.now().strftime("%Y%m%d")
    print("=== LINEステップメール連動型メルマガ生成 %s ===" % datetime.now().strftime("%Y-%m-%d %H:%M"))

    progress = load_progress()
    phase, number = progress["phase"], progress["number"]
    total = progress.get("total_sent", 0)
    print("  本日の話：%s-%02d（通算%d通目）" % (phase, number, total + 1))

    line_content = load_line_content(phase, number)
    if not line_content:
        print("  ❌ ファイルなし：%s-%02d" % (phase, number))
        return
    print("  ✅ LINE読み込み完了（%d字）" % len(line_content))

    print("  🔍 最新AI情報収集中...")
    ai_news = get_latest_ai_news()
    print("  ✅ AI情報取得完了")

    print("  ✍️  メルマガ執筆中...")
    merumaga = generate_merumaga(line_content, phase, number, ai_news)
    print("  ✅ メルマガ執筆完了（%d字）" % len(merumaga))

    # TXT保存
    labels = {"P": "プロローグ", "Q": "絞り込み", "U": "共感", "E": "教育", "S": "刺激", "T": "行動促進"}
    txt_name = "メルマガ_%s_%s-%02d.txt" % (today, phase, number)
    txt_path = os.path.join(OUTPUT_DIR, txt_name)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("レベルファイブ AI経営マスタリー メルマガ\n")
        f.write("%s %s-%02d | %s\n\n" % (labels.get(phase, phase), phase, number, today))
        f.write(merumaga)
    print("  ✅ TXT保存：%s" % txt_name)

    # MD保存
    md_name = txt_name.replace(".txt", ".md")
    md_path = os.path.join(OUTPUT_DIR, md_name)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# レベルファイブ AI経営マスタリー メルマガ\n")
        f.write("## %s %s-%02d | %s\n\n" % (labels.get(phase, phase), phase, number, today))
        f.write(merumaga)
    print("  ✅ MD保存：%s" % md_name)

    # 進捗更新
    next_p = next_progress(progress)
    save_progress(next_p)
    print("  📍 次回：%s-%02d" % (next_p["phase"], next_p["number"]))
    print("\n=== 完了 %s-%02d ===" % (phase, number))

if __name__ == "__main__":
    main()
