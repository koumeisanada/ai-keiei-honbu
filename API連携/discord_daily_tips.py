#!/usr/bin/env python3
# Discord AIノウハウ 毎日自動投稿スクリプト（カウンター管理版）
import sys, traceback
from pathlib import Path
from datetime import datetime

LOG_PATH = Path.home() / "Desktop/AI経営本部/API連携/discord_tips.log"

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = "[%s] %s" % (timestamp, msg)
    print(line)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")

try:
    log("=== Discord Tips 投稿開始 ===")
    sys.path.insert(0, str(Path.home() / "Desktop/AI経営本部/API連携"))
    from discord_post import post_to_discord
    from discord_tips_library import get_today_tip

    tip, num = get_today_tip()
    log("今日のTips: #%d" % num)
    post_to_discord(tip)
    log("✅ Tips #%d 投稿完了" % num)
    log("=== 完了 ===")

except Exception as e:
    log("❌ エラー発生: %s" % e)
    log(traceback.format_exc())
    sys.exit(1)
