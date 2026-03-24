# ====================================
# ケイタ式 eBay→メルカリ・ヤフオク 自動リサーチシステム
#
# 使い方：
# ケイタ式で実績のある商品キーワードを
# RESEARCH_TARGETSに追加して実行する
#
# 例：
# {"keyword": "vintage camera Japan", "ebay_category": "cameras"}
# ↑eBayで実際に売れた商品のキーワードを入力
#
# 実行コマンド：
# python3 ~/Desktop/AI経営本部/物販ビジネス/ケイタ式/自動化スクリプト/ebay_japan_research.py
# ====================================

import os
import time
import json
from datetime import datetime
from google import genai
from google.genai import types

gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SAVE_DIR = os.path.expanduser(
    "~/Desktop/AI経営本部/物販ビジネス/ケイタ式/リサーチ結果"
)

def get_ebay_sold_items(keywords, limit=20):
    print(f"\neBay売れ筋リサーチ中：{keywords}")
    prompt = f"""
eBayで最近売れた日本の商品を調査してください。
検索キーワード：{keywords}
カテゴリ：日本から輸出された中古品

以下を調査：
1. 最近売れた価格帯（sold listings）
2. 人気の商品状態
3. 平均落札価格・最高・最低
4. 人気キーワード
5. 売れるまでの期間

JSON形式で出力：
{{"keyword":"{keywords}","average_price_usd":数値,"price_range":{{"min":数値,"max":数値}},"popular_conditions":["状態"],"popular_keywords":["キーワード"],"sale_speed":"期間","total_sold":数値,"items":[{{"title":"商品名","sold_price_usd":数値,"condition":"状態","sold_date":"日付"}}]}}
"""
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt,
            config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())]))
        text = response.text
        start = text.find('{'); end = text.rfind('}') + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
        return {"keyword": keywords, "raw_result": text}
    except Exception as e:
        return {"keyword": keywords, "error": str(e)}

def research_mercari(keywords, ebay_price_usd):
    print(f"\nメルカリリサーチ中：{keywords}")
    usd_to_jpy = 150
    target = int(ebay_price_usd * usd_to_jpy * 0.3)
    prompt = f"""
メルカリで以下の商品を調査してください。
検索キーワード：{keywords}
eBay売値：${ebay_price_usd}（約{int(ebay_price_usd*usd_to_jpy)}円）
目標仕入れ価格：{target}円以下

調査：出品価格帯・売切れ価格・在庫状況・おすすめ検索キーワード

JSON形式で出力：
{{"keyword":"{keywords}","target_buy_price_jpy":{target},"availability":"豊富/普通/少ない","recommended_search_keywords":["キーワード"],"best_deal_estimate":"見込み","profit_estimate_jpy":数値,"current_listings":[{{"title":"商品名","price_jpy":数値,"condition":"状態"}}]}}
"""
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt,
            config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())]))
        text = response.text
        start = text.find('{'); end = text.rfind('}') + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
        return {"keyword": keywords, "raw_result": text}
    except Exception as e:
        return {"keyword": keywords, "error": str(e)}

def research_yahooauction(keywords, ebay_price_usd):
    print(f"\nヤフオクリサーチ中：{keywords}")
    usd_to_jpy = 150
    target = int(ebay_price_usd * usd_to_jpy * 0.3)
    prompt = f"""
ヤフオクで以下の商品を調査してください。
検索キーワード：{keywords}
eBay売値：${ebay_price_usd}（約{int(ebay_price_usd*usd_to_jpy)}円）
目標仕入れ価格：{target}円以下

調査：入札状況・落札価格・在庫状況・おすすめキーワード・狙い目時間帯

JSON形式で出力：
{{"keyword":"{keywords}","target_buy_price_jpy":{target},"availability":"豊富/普通/少ない","recommended_search_keywords":["キーワード"],"best_time_to_bid":"時間帯","profit_estimate_jpy":数値,"current_auctions":[{{"title":"商品名","current_price_jpy":数値,"end_time":"時間","bid_count":数値}}]}}
"""
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt,
            config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())]))
        text = response.text
        start = text.find('{'); end = text.rfind('}') + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
        return {"keyword": keywords, "raw_result": text}
    except Exception as e:
        return {"keyword": keywords, "error": str(e)}

def generate_report(keyword, ebay_data, mercari_data, yahoo_data):
    prompt = f"""
以下のリサーチデータを元に物販ビジネスの仕入れ判断レポートを作成してください。

【eBay】{json.dumps(ebay_data, ensure_ascii=False, indent=2)[:1500]}
【メルカリ】{json.dumps(mercari_data, ensure_ascii=False, indent=2)[:1500]}
【ヤフオク】{json.dumps(yahoo_data, ensure_ascii=False, indent=2)[:1500]}

出力：
# {keyword} リサーチレポート
## 総合判定（★1〜5）
## 価格サマリー（表形式：eBay売値・メルカリ仕入れ・ヤフオク仕入れ・想定利益・利益率）
## メルカリ仕入れ情報
## ヤフオク仕入れ情報
## 仕入れ推奨コンディション
## アクションプラン
"""
    response = gemini_client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text

RESEARCH_TARGETS = [
    {"keyword": "vintage camera Japan", "ebay_category": "cameras"},
    {"keyword": "Japanese vintage watch", "ebay_category": "watches"},
    {"keyword": "Nintendo game Japan", "ebay_category": "games"},
    {"keyword": "Japanese anime figure", "ebay_category": "figures"},
    {"keyword": "Japanese vintage toy", "ebay_category": "toys"},
]

def main():
    today = datetime.now().strftime("%Y%m%d")
    today_jp = datetime.now().strftime("%Y年%m月%d日")
    os.makedirs(SAVE_DIR, exist_ok=True)

    print("=" * 60)
    print("ケイタ式 eBay→メルカリ・ヤフオク 自動リサーチシステム")
    print(f"実行日：{today_jp}")
    print("=" * 60)

    all_results = []
    for target in RESEARCH_TARGETS:
        keyword = target["keyword"]
        print(f"\n{'='*40}\nリサーチ対象：{keyword}\n{'='*40}")

        ebay_data = get_ebay_sold_items(keyword)
        time.sleep(2)

        ebay_price = 50
        if isinstance(ebay_data, dict):
            ebay_price = ebay_data.get("average_price_usd", 50)
            if not isinstance(ebay_price, (int, float)):
                ebay_price = 50

        mercari_data = research_mercari(keyword, ebay_price)
        time.sleep(2)

        yahoo_data = research_yahooauction(keyword, ebay_price)
        time.sleep(2)

        report = generate_report(keyword, ebay_data, mercari_data, yahoo_data)
        all_results.append({"keyword": keyword, "report": report})

        report_file = os.path.join(SAVE_DIR, f"{today}_{keyword.replace(' ', '_')}_リサーチ.md")
        with open(report_file, "w") as f:
            f.write(report)
        print(f"✅ レポート保存：{report_file}")

    summary_prompt = f"""
以下の全リサーチ結果を元に本日の仕入れ候補ランキングを作成してください。
キーワード数：{len(all_results)}件
{chr(10).join([r.get('report','')[:500] for r in all_results])}

出力：
# 本日の仕入れ候補ランキング {today_jp}
## 仕入れ推奨順位（表形式：順位・商品・推奨度・想定利益・仕入先・理由）
## 今日すぐ行動すべきこと
## 明日以降のリサーチ候補
## 注意事項
"""
    summary = gemini_client.models.generate_content(model="gemini-2.5-flash", contents=summary_prompt).text
    summary_file = os.path.join(SAVE_DIR, f"{today}_本日の仕入れ候補ランキング.md")
    with open(summary_file, "w") as f:
        f.write(summary)

    print(f"\n{'='*60}\n✅ 全リサーチ完了！\n{'='*60}")
    print(f"保存先：{SAVE_DIR}")
    print(f"仕入れ候補ランキング：{summary_file}")

if __name__ == "__main__":
    main()
