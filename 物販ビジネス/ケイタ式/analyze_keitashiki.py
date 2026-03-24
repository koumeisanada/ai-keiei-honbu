from google import genai
from google.genai import types
import os
import glob
from datetime import datetime

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

RESOURCE_DIR = os.path.expanduser(
    "~/Desktop/AI経営本部/物販ビジネス/ケイタ式/資料"
)
SAVE_DIR = os.path.expanduser(
    "~/Desktop/AI経営本部/物販ビジネス/ケイタ式/AI自動化分析"
)

def load_all_materials():
    all_text = ""
    files = []
    for ext in ['*.txt', '*.md']:
        files.extend(glob.glob(f"{RESOURCE_DIR}/**/{ext}", recursive=True))
    files = sorted(set(files))
    for f in files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read()
                all_text += f"\n\n=== {os.path.basename(f)} ===\n{content[:500]}"
        except Exception as e:
            pass
    print(f"✅ {len(files)}ファイル読み込み完了")
    return all_text, len(files)

def analyze_business_model(materials):
    prompt = f"""
以下はケイタ式（国内仕入・海外輸出販売）の物販ビジネスの資料です。

{materials[:8000]}

以下を分析してください。

## 1. ケイタ式ビジネスモデルの全工程マップ
ビジネスの開始から売上回収までの全工程を時系列で全て抽出。
各工程：工程名・具体的な作業内容・所要時間目安・必要スキル・課題

## 2. AI・自動化による効率化分析
各工程を4分類：
【完全自動化可能】→実装難易度・時間削減率
【部分自動化可能】→AI担当部分・人間判断部分
【AI補助のみ】→有効なAI補助
【人間必須】→理由

## 3. 自動化優先度ランキング
効果÷難易度で上位10工程をランキング表

## 4. 即座に実装できる自動化TOP3
Claude Codeで今すぐ実装できるスクリプトアイデア3つ

## 5. 3大AIの活用提案
Claude・Gemini・ChatGPTの各AIを
ケイタ式のどの工程にどう活用するか

## 6. 月間の時間削減試算
全自動化を実装した場合の月間時間削減試算（表形式）

日本語で出力してください。
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        return response.text
    except Exception:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

def main():
    today = datetime.now().strftime("%Y年%m月%d日")
    os.makedirs(SAVE_DIR, exist_ok=True)

    print("=" * 60)
    print("ケイタ式 AI自動化分析 開始")
    print("=" * 60)

    materials, file_count = load_all_materials()

    print(f"分析中...（{file_count}ファイルの資料を基に）")
    analysis = analyze_business_model(materials)

    output_file = os.path.join(SAVE_DIR, f"AI自動化分析レポート_{datetime.now().strftime('%Y%m%d')}.md")
    with open(output_file, "w") as f:
        f.write(f"# ケイタ式 AI自動化分析レポート\n")
        f.write(f"## 分析日：{today}\n")
        f.write(f"## 分析対象：{file_count}ファイル\n\n---\n\n")
        f.write(analysis)

    print(f"✅ 分析完了：{output_file}")

if __name__ == "__main__":
    main()
