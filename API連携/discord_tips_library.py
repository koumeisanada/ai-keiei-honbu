#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Discord AI Tips コンテンツライブラリ
# 最終更新：2026-04-04

import json
from pathlib import Path

BASE = Path.home() / "Desktop/AI経営本部/API連携"
TIPS_FILE = BASE / "discord_tips_data.json"
COUNTER_FILE = BASE / "discord_tips_counter.json"

def load_tips():
    with open(TIPS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

TIPS = load_tips()

def get_today_tip():
    if COUNTER_FILE.exists():
        data = json.loads(COUNTER_FILE.read_text())
        idx = data.get("index", 0)
    else:
        idx = 0
    tip = TIPS[idx % len(TIPS)]
    new_idx = (idx + 1) % len(TIPS)
    COUNTER_FILE.write_text(json.dumps({"index": new_idx}))
    return tip, idx + 1
