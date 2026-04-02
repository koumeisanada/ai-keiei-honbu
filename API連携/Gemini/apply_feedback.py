from google import genai
import os
import glob
from datetime import datetime

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", "")))

def get_latest_feedback():
    base = os.path.expanduser("~/Desktop/AI経営本部/集客販売/日次成果物")
    folders = sorted(glob.glob(f"{base}/*/"), reverse=True)

    for folder in folders:
        feedback_file = os.path.join(folder, "品質チェック結果.txt")
        if os.path.exists(feedback_file):
            try:
                with open(feedback_file, "r") as f:
                    return f.read()
            except OSError as e:
                print(f"⚠️ フィードバック読み込みスキップ: {feedback_file} ({e})")
                continue
    return None

def apply_feedback_to_skill(feedback):
    skill_path = os.path.expanduser(
        "~/Desktop/AI経営本部/集客販売/メルマガ原稿/SKILL_メルマガ自動生成.md"
    )

    with open(skill_path, "r") as f:
        current_skill = f.read()

    prompt = f"""以下の品質チェック結果を分析して、
SKILLファイルの改善点を抽出してください。

【品質チェック結果】
{feedback}

【現在のSKILLファイル】
{current_skill[:3000]}

以下の形式で出力してください：
1. 改善すべき点（箇条書き）
2. SKILLファイルへの追記内容（そのまま追記できる形式で）"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )

    improvements_path = os.path.expanduser(
        "~/Desktop/AI経営本部/集客販売/メルマガ原稿/SKILL_改善履歴.md"
    )

    today = datetime.now().strftime("%Y年%m月%d日")
    with open(improvements_path, "a") as f:
        f.write(f"\n\n## {today}の改善内容\n")
        f.write(response.text)

    print("✅ 品質チェック結果をSKILLファイルに反映しました")
    print(response.text)

if __name__ == "__main__":
    feedback = get_latest_feedback()
    if feedback:
        apply_feedback_to_skill(feedback)
    else:
        print("品質チェック結果が見つかりませんでした")
