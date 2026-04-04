#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Discord AI Tips コンテンツライブラリ
# 最終更新：2026-04-04

import json
from pathlib import Path

BASE = Path.home() / "Desktop/AI経営本部/API連携"
TIPS_FILE = BASE / "discord_tips_data.json"
COUNTER_FILE = BASE / "discord_tips_counter.json"
POSTED_FILE = BASE / "discord_tips_posted.json"

def load_tips():
    with open(TIPS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

TIPS = load_tips()

def load_posted():
    if POSTED_FILE.exists():
        return json.loads(POSTED_FILE.read_text())
    return []

def save_posted(posted):
    POSTED_FILE.write_text(json.dumps(posted, ensure_ascii=False))

def get_today_tip():
    if COUNTER_FILE.exists():
        data = json.loads(COUNTER_FILE.read_text())
        idx = data.get("index", 0)
    else:
        idx = 0

    posted = load_posted()

    # 投稿済みのTipsをスキップ（最大Tips数まで試行）
    for _ in range(len(TIPS)):
        tip = TIPS[idx % len(TIPS)]
        tip_id = tip[:50]  # 先頭50文字をIDとして使用
        if tip_id not in posted:
            # 未投稿のTipsを発見
            posted.append(tip_id)
            save_posted(posted)
            new_idx = (idx + 1) % len(TIPS)
            COUNTER_FILE.write_text(json.dumps({"index": new_idx}))
            return tip, idx + 1
        idx = (idx + 1) % len(TIPS)

    # 全Tips投稿済みの場合はリセットして最初から
    save_posted([])
    tip = TIPS[0]
    COUNTER_FILE.write_text(json.dumps({"index": 1}))
    posted_new = [tip[:50]]
    save_posted(posted_new)
    return tip, 1
