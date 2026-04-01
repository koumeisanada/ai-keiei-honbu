#!/usr/bin/env python3
import sys
sys.path.insert(0, "/Users/sanadahiroaki/Desktop/AI経営本部/API連携")
from discord_post import post_to_discord
from discord_tips_library import get_today_tip

def main():
    tip, idx = get_today_tip()
    print("Discord投稿: AIノウハウ Tips #%d" % idx)
    post_to_discord(tip)

if __name__ == "__main__":
    main()
