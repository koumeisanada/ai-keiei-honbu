#!/usr/bin/env python3
import os, sys, json, subprocess, hashlib
from pathlib import Path
from datetime import datetime

BASE = Path.home() / "Desktop/AI経営本部"
KB_DIR = BASE / "知識ベース"
OUTPUT_PATH = BASE / "スキル/SKILL_統合知識ベース.md"
LOG_PATH = BASE / "API連携/knowledge_build.log"
INDEX_PATH = BASE / "API連携/knowledge_index.json"

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = "[%s] %s" % (timestamp, msg)
    print(line)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def build_knowledge_base():
    log("=== 知識ベース構築開始 ===")
    if INDEX_PATH.exists():
        index = json.load(open(INDEX_PATH))
    else:
        index = {}

    md_files = sorted(KB_DIR.rglob("*.md"))
    md_files = [f for f in md_files if f.name != "README.md"]

    if not md_files:
        log("知識ベースにMDファイルが見つかりません")
        return

    log("発見したMDファイル: %d件" % len(md_files))

    new_index = {}
    changed_files = []
    for f in md_files:
        h = hashlib.md5(open(f, "rb").read()).hexdigest()
        new_index[str(f)] = h
        if index.get(str(f)) != h:
            changed_files.append(f)

    if not changed_files and OUTPUT_PATH.exists():
        log("変更なし。ビルドをスキップ")
        return

    log("更新・追加ファイル: %d件" % len(changed_files))

    sections = []
    sections.append("# アイム 統合知識ベース\n# 最終更新：%s\n# ファイル数：%d件\n---\n" % (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), len(md_files)))

    for md_file in md_files:
        try:
            content = open(md_file, encoding="utf-8").read()
            category = md_file.parent.name
            sections.append("\n## 【%s】%s\n\n%s\n\n---\n" % (category, md_file.stem, content))
        except Exception as e:
            log("読み込みエラー: %s - %s" % (md_file.name, e))

    output = "\n".join(sections)
    os.makedirs(OUTPUT_PATH.parent, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(output)
    log("統合SKILLファイル生成完了: %d文字" % len(output))

    with open(INDEX_PATH, "w") as f:
        json.dump(new_index, f, ensure_ascii=False, indent=2)

    # アイムBot再起動
    plist = Path.home() / "Library/LaunchAgents/com.ai-keiei-honbu.discord-aim-bot.plist"
    if plist.exists():
        subprocess.run(["launchctl", "unload", str(plist)], capture_output=True)
        import time; time.sleep(2)
        subprocess.run(["launchctl", "load", str(plist)], capture_output=True)
        log("アイムBot再起動完了")

    # GitHub保存
    for cmd in [
        ["git", "-C", str(BASE), "add", "知識ベース/", "スキル/SKILL_統合知識ベース.md", "API連携/knowledge_index.json"],
        ["git", "-C", str(BASE), "commit", "-m", "feat: 知識ベース更新 %s" % datetime.now().strftime("%Y-%m-%d %H:%M")],
        ["git", "-C", str(BASE), "push", "origin", "main"],
    ]:
        subprocess.run(cmd, capture_output=True, text=True)

    log("=== 知識ベース構築完了 ===")

if __name__ == "__main__":
    build_knowledge_base()
