from google import genai
import os
import sys

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", "")))

def generate_line_4days(merumaga_text):
    """メルマガ原稿からLINEステップメール4通を生成する"""
    prompt = f"""あなたは真田孔明（北の株式投資大学）のLINEメッセージライターです。

以下のメルマガ原稿をもとに、LINEステップメール用の原稿を4通作成してください。

【ルール】
・1通あたり900〜1000文字（厳守）
・です・ます調で統一
・一人称は「僕」（「私」は使わない）
・1文は短く（20字以内が理想）
・改行多め・空行多め（縦に読ませる）
・年号・具体的な日付・季節ネタを除去してエバーグリーンな内容にする
・時事的表現は普遍的な表現に変換する（例：「2026年の〜」→「今の〜」）
・成功シンドロームOSの視点（OSなき者にアプリは動かない）を自然な形で入れる
・絵文字は使わない
・AIが書いたとバレる表現（「〜でしょう」「〜と言えます」など機械的な表現）は使わない

【4通の構成】
■通1（序論ベース）：「つかみ・問題提起」
- メルマガ序論の核心をLINEサイズに圧縮
- 冒頭1文で「これは自分の話だ」と思わせる
- 読者の痛みを刺す問いかけ
- 末尾：「次回、この続きをお伝えします。」

■通2（本論①ベース）：「理論と教育」
- メルマガ本論①の核心知識をLINEサイズに圧縮
- R>G・数字・法則を使って教育する
- 「僕たち」目線で語る
- 末尾：「明日はこれを解決する方法をお伝えします。」

■通3（本論②ベース）：「事例と刺激」
- 成功事例（U君・ケイタ社長・O氏・マスターヒロなど）を使う
- 「あなたも同じ立場だった」共感から始める
- 「自分にもできる」という確信を植え付ける
- 末尾：「次回、具体的な一歩をお伝えします。」

■通4（結論CTAベース）：「行動喚起」
- 「今すぐ始める理由」を3つの角度で訴える
- 緊急性・希少性を盛り込む
- 北の株式投資大学または地下ソサエティへの誘導
- 末尾：「まずは無料のZOOMセミナーで話を聞いてみてください。」

【出力形式】
各通の冒頭に「【通1】」「【通2】」「【通3】」「【通4】」と表示して、
それぞれ900〜1000文字で出力すること。

【元のメルマガ原稿】
{merumaga_text}"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text


if __name__ == "__main__":
    # 引数からメルマガテキストを受け取る（パイプ or ファイル）
    if len(sys.argv) > 1:
        merumaga_file = sys.argv[1]
        with open(merumaga_file, "r", encoding="utf-8") as f:
            merumaga_text = f.read()
    else:
        # 標準入力から読む
        merumaga_text = sys.stdin.read()

    result = generate_line_4days(merumaga_text)
    print(result)
