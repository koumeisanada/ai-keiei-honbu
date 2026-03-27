#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
セールスレター AIマネージャー ― Claude Code実行版
=================================================
使い方:
  python3 generate_salesletter_review.py --mode review --input salesletter_draft.txt
  python3 generate_salesletter_review.py --mode write  --theme "AI講座の必要性"
  python3 generate_salesletter_review.py --mode check  --input salesletter_v3.txt
  python3 generate_salesletter_review.py --mode finish --input salesletter_v5.txt

モード:
  review  - 草稿をQUEST/ブレット/マインドセットの3軸でレビュー
  write   - テーマからセールスレター本文を生成
  check   - チェックリスト12項目で確認
  finish  - 最終仕上げ（磨き込み・表現強化）
"""

import os
import sys
import argparse
import pathlib
from datetime import datetime
import anthropic

# ========== 設定 ==========
SKILL_PATH = pathlib.Path.home() / "Desktop" / "AI経営本部" / "集客販売" / "セールスレター" / "マスター文書" / "SKILL_セールスレター統合完全版.md"
OUTPUT_DIR = pathlib.Path.home() / "Desktop" / "AI経営本部" / "集客販売" / "セールスレター" / "日次成果物"

MODEL = "claude-opus-4-6"  # セールスレターは最高品質モデル使用

def load_skill() -> str:
    """SKILLファイルを読み込む"""
    if SKILL_PATH.exists():
        return SKILL_PATH.read_text(encoding="utf-8")
    else:
        print(f"⚠️  SKILLファイルが見つかりません: {SKILL_PATH}")
        print("   先に save_salesletter_skill.py を実行してください")
        sys.exit(1)

def load_input_file(path: str) -> str:
    """入力ファイルを読み込む"""
    p = pathlib.Path(path)
    if not p.exists():
        print(f"❌ ファイルが見つかりません: {path}")
        sys.exit(1)
    return p.read_text(encoding="utf-8")

def save_output(content: str, mode: str) -> pathlib.Path:
    """成果物を保存する"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"SL_{mode}_{ts}.md"
    out_path = OUTPUT_DIR / filename
    out_path.write_text(content, encoding="utf-8")
    return out_path

def build_system_prompt(skill: str) -> str:
    return f"""あなたは真田孔明のセールスレター AIマネージャーです。
以下のSKILLを完全に習得・内在化した状態で動作してください。

{skill}

【絶対厳守】
- 一人称は「僕」
- です・ます調
- 架空の成功事例・誇張・内輪言葉禁止
- 日時指定言語禁止（「本日限り」等）
- 技術フレームワーク名・設計哲学は外部文書に記載禁止
- AIが作ったことがバレる文体禁止
"""

def run_review(skill: str, draft: str) -> str:
    """草稿レビューモード"""
    client = anthropic.Anthropic()
    prompt = f"""以下のセールスレター草稿を、QUEST構成・ブレットの質・マインドセットの3軸でレビューしてください。

改善点を箇条書きで提示し、各項目に「優先度：高/中/低」を付けてください。
最後に総合評価（100点満点）を出してください。

【草稿】
{draft}
"""
    msg = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        system=build_system_prompt(skill),
        messages=[{"role": "user", "content": prompt}]
    )
    return msg.content[0].text

def run_write(skill: str, theme: str) -> str:
    """新規セールスレター生成モード"""
    client = anthropic.Anthropic()
    prompt = f"""以下のテーマでセールスレターを書いてください。

テーマ：{theme}

QUEST構成（Q→U→E→S→T）に厳密に従い、
- 各セクション約1,000文字
- 全体4,000文字目安
- ブレット15個以上（S：Stimulateパート）
- 追伸に思い・理念・殺し文句の3要素を含む

真田孔明スタイルで書いてください。
"""
    msg = client.messages.create(
        model=MODEL,
        max_tokens=6000,
        system=build_system_prompt(skill),
        messages=[{"role": "user", "content": prompt}]
    )
    return msg.content[0].text

def run_check(skill: str, draft: str) -> str:
    """チェックリスト確認モード"""
    client = anthropic.Anthropic()
    prompt = f"""以下のセールスレターを、SKILLのチェックリスト12項目で確認してください。

各項目に ✅ または ❌ をつけ、❌の場合は具体的な改善案を提示してください。

【草稿】
{draft}
"""
    msg = client.messages.create(
        model=MODEL,
        max_tokens=3000,
        system=build_system_prompt(skill),
        messages=[{"role": "user", "content": prompt}]
    )
    return msg.content[0].text

def run_finish(skill: str, draft: str) -> str:
    """最終仕上げモード"""
    client = anthropic.Anthropic()
    prompt = f"""以下のセールスレターを最終仕上げしてください。

仕上げの観点：
1. 文学スキルを使い感情を動かす表現に磨く
2. ブレットをより弾丸力の高い文章に強化する
3. 追伸を「思い・理念・殺し文句」の3要素で完成させる
4. 全体の流れをQUESTに沿って整える
5. 「AIが書いた感」を完全に消す

元の草稿の骨格は維持しつつ、表現を全面的に磨いた完成版を出力してください。

【草稿】
{draft}
"""
    msg = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        system=build_system_prompt(skill),
        messages=[{"role": "user", "content": prompt}]
    )
    return msg.content[0].text

def main():
    parser = argparse.ArgumentParser(description="セールスレター AIマネージャー")
    parser.add_argument("--mode", required=True, choices=["review", "write", "check", "finish"],
                        help="実行モード")
    parser.add_argument("--input", help="入力ファイルパス（review/check/finishモード）")
    parser.add_argument("--theme", help="テーマ（writeモード）")
    args = parser.parse_args()

    print(f"🚀 セールスレター AIマネージャー起動 [モード: {args.mode}]")
    print(f"📚 SKILLファイル読み込み中...")
    skill = load_skill()
    print(f"   ✅ SKILL読み込み完了 ({len(skill):,} 文字)")

    if args.mode == "write":
        if not args.theme:
            print("❌ --theme を指定してください")
            sys.exit(1)
        print(f"✍️  セールスレター生成中...")
        result = run_write(skill, args.theme)

    elif args.mode == "review":
        if not args.input:
            print("❌ --input を指定してください")
            sys.exit(1)
        draft = load_input_file(args.input)
        print(f"🔍 草稿レビュー中...")
        result = run_review(skill, draft)

    elif args.mode == "check":
        if not args.input:
            print("❌ --input を指定してください")
            sys.exit(1)
        draft = load_input_file(args.input)
        print(f"✅ チェックリスト確認中...")
        result = run_check(skill, draft)

    elif args.mode == "finish":
        if not args.input:
            print("❌ --input を指定してください")
            sys.exit(1)
        draft = load_input_file(args.input)
        print(f"✨ 最終仕上げ中...")
        result = run_finish(skill, draft)

    out_path = save_output(result, args.mode)
    print(f"\n{'='*60}")
    print(f"✅ 完了！")
    print(f"📄 保存先: {out_path}")
    print(f"{'='*60}")
    print(result[:500] + "...\n（以下省略 — ファイルを確認してください）")

if __name__ == "__main__":
    main()
