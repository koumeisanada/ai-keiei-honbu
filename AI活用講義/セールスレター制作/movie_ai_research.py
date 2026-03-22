from google import genai
from google.genai import types
import os
from datetime import datetime

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SAVE_DIR = os.path.expanduser(
    "~/Desktop/AI経営本部/AI活用講義/セールスレター制作/06_競合分析統合"
)

prompt = """
古今東西の映画・ドラマ・アニメ・小説・漫画の中で
「主人公がAI・テクノロジー・自動化システムを活用して
問題を解決したり・目標を達成したり・自分をパワーアップさせた」
作品・シーンを調査してください。

【調査対象】
・日本のアニメ・漫画・ドラマ・映画
・米国・欧州の映画・ドラマ・小説
・韓国・中国・アジア圏の作品も含める
・実写・アニメ・CGどちらでも可
・AIに限らず「自動化・組織・システム」を使って
　個人が大きな力を得た作品も含める

【出力形式】
各作品について以下を書き出してください。

## 作品名（国・年代・ジャンル）

### 主人公の状況（出発点）
どんな状況・問題を抱えていたか

### AIの活用方法
どのようにAI・テクノロジー・システムを使ったか

### 達成した目的・成果
何を成し遂げたか

### セールスレターへの転用ポイント
真田孔明のAI講座のどのパートに使えるか
具体的な転用フレーズ案

---

【特に重視する作品パターン】
1. 普通の一般人がAIで変身・覚醒するパターン
2. 素人・初心者がAIで専門家を超えるパターン
3. 一人が組織・チームと同等の力を得るパターン
4. 時間・場所の制約からAIで解放されるパターン
5. AIが「仲間・相棒・組織」として機能するパターン
6. 劣勢の主人公がAIで逆転するパターン
7. AIで自分の弱点を補完して強みを最大化するパターン

できる限り多くの作品をピックアップすること。
最低30作品以上を目標にすること。

日本語で出力すること。
各作品の転用ポイントを必ず含めること。
"""

print("映画・ドラマ・アニメのAI活用パターンをリサーチ中...")

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

os.makedirs(SAVE_DIR, exist_ok=True)
output_file = os.path.join(
    SAVE_DIR,
    f"映画ドラマアニメ_AI活用パターン研究.md"
)

content = "# 映画・ドラマ・アニメ AI活用パターン研究\n"
content += f"## 調査日：{datetime.now().strftime('%Y年%m月%d日')}\n"
content += "## 目的：セールスレターの共感・刺激パートへの転用\n\n"
content += "---\n\n"
content += response.text

with open(output_file, "w") as f:
    f.write(content)

print(f"✅ 保存完了：{output_file}")

import subprocess
subprocess.run([
    "bash", "-c",
    f"cd ~/Desktop/AI経営本部 && "
    f"git add AI活用講義/セールスレター制作/06_競合分析統合/ && "
    f"git commit -m '映画ドラマアニメAI活用パターン研究完了' && "
    f"git push origin salesletter-development"
])

print("✅ GitHubプッシュ完了")
print(f"確認URL：https://github.com/koumeisanada/ai-keiei-honbu/blob/salesletter-development/AI活用講義/セールスレター制作/06_競合分析統合/映画ドラマアニメ_AI活用パターン研究.md")
