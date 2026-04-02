#!/usr/bin/env python3
"""強化版 米国株リサーチ（セミナー向け・出典付き・重複排除）"""
import os, json, sys, time
from datetime import datetime, timedelta

BASE = os.path.expanduser("~/Desktop/AI経営本部")
API_DIR = os.path.join(BASE, "API連携")
OUTPUT_DIR = os.path.join(BASE, "リサーチ出力")
os.makedirs(OUTPUT_DIR, exist_ok=True)
DEDUP_DB = os.path.join(API_DIR, "research_history.json")

TARGET_COMPANIES = [
    {"name": "NVIDIA", "ticker": "NVDA", "theme": "AI・GPU・データセンター"},
    {"name": "Apple", "ticker": "AAPL", "theme": "iPhone・サービス・AI統合"},
    {"name": "Microsoft", "ticker": "MSFT", "theme": "Azure・Copilot・AI企業向け"},
    {"name": "Alphabet（Google）", "ticker": "GOOGL", "theme": "検索AI・Gemini・広告"},
    {"name": "Meta", "ticker": "META", "theme": "SNS・Llama・AR/VR"},
    {"name": "Amazon", "ticker": "AMZN", "theme": "AWS・EC・AI投資"},
    {"name": "Tesla", "ticker": "TSLA", "theme": "EV・FSD・Optimus・SpaceX関連"},
    {"name": "Netflix", "ticker": "NFLX", "theme": "動画・広告・AI活用"},
    {"name": "Anthropic", "ticker": "（非上場）", "theme": "Claude・AI安全性"},
]

def load_history():
    if os.path.exists(DEDUP_DB):
        return json.load(open(DEDUP_DB))
    return {"published": []}

def save_history(history):
    with open(DEDUP_DB, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def is_duplicate(topic, history):
    cutoff = datetime.now() - timedelta(days=7)
    for item in history["published"]:
        dt = datetime.fromisoformat(item["date"])
        if dt > cutoff and topic[:30] in item.get("topic", ""):
            return True
    return False

def add_to_history(topic, history):
    history["published"].append({"date": datetime.now().isoformat(), "topic": topic})
    cutoff = datetime.now() - timedelta(days=7)
    history["published"] = [h for h in history["published"] if datetime.fromisoformat(h["date"]) > cutoff]
    return history

def research_with_gemini(company):
    try:
        import google.genai as genai
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
        prompt = "直近7日以内の「%s（%s）」に関する最新情報。テーマ：%s。出典（メディア名・日付）を必ず明記。カテゴリ別（決算/製品/経営陣発言/アナリスト評価/競合動向/規制リスク）で分類。各情報に投資家への示唆を付記。" % (company["name"], company["ticker"], company["theme"])
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text
    except Exception as e:
        return "Geminiエラー：%s" % e

def analyze_with_claude(company, raw_research):
    try:
        import anthropic
        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            system="あなたは北の株式投資大学のリサーチアナリスト。250名の投資コミュニティ向けに深い考察を提供。投資アドバイスではなく考察の材料として。数字と根拠で語る。出典を必ず明記。",
            messages=[{"role": "user", "content": "以下のリサーチ情報を元にセミナー向け考察レポートを作成。\n企業：%s（%s）テーマ：%s\n\n収集情報：\n%s\n\n構成：1.今週の最重要ニュース（出典付き3つ以内）2.数字で見る変化 3.大衆に見えていない考察ポイント 4.AI革命全体との連動性 5.セミナーで問いかけるべき論点" % (company["name"], company["ticker"], company["theme"], raw_research[:3000])}]
        )
        return response.content[0].text
    except Exception as e:
        return "Claudeエラー：%s" % e

def main():
    print("=== 強化版米国株リサーチ開始 %s ===" % datetime.now().strftime("%Y-%m-%d %H:%M"))
    history = load_history()
    today = datetime.now().strftime("%Y%m%d")
    all_reports = []

    for company in TARGET_COMPANIES:
        print("\n📊 %s リサーチ中..." % company["name"])
        if is_duplicate(company["name"], history):
            print("  ⏭ 過去7日以内に掲載済み → スキップ")
            continue
        print("  🔍 Geminiでリサーチ...")
        raw = research_with_gemini(company)
        print("  🧠 Claudeで考察...")
        report = analyze_with_claude(company, raw)
        all_reports.append({"company": company["name"], "ticker": company["ticker"], "theme": company["theme"], "report": report})
        history = add_to_history(company["name"], history)
        time.sleep(2)

    if not all_reports:
        print("\n⚠ 全企業が重複または取得不可")
        return

    md = "# 米国株考察セミナー リサーチレポート\n# 生成：%s\n---\n\n" % datetime.now().strftime("%Y年%m月%d日 %H:%M")
    for r in all_reports:
        md += "## %s（%s）\nテーマ：%s\n\n%s\n\n---\n\n" % (r["company"], r["ticker"], r["theme"], r["report"])

    md_path = os.path.join(OUTPUT_DIR, "米国株リサーチ_%s.md" % today)
    txt_path = os.path.join(OUTPUT_DIR, "米国株リサーチ_%s.txt" % today)
    with open(md_path, "w", encoding="utf-8") as f: f.write(md)
    with open(txt_path, "w", encoding="utf-8") as f: f.write(md.replace("#","").replace("**",""))
    save_history(history)
    print("\n✅ レポート保存完了：%d社 / %s字" % (len(all_reports), "{:,}".format(len(md))))

if __name__ == "__main__":
    main()
