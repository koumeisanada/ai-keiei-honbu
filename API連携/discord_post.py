import sys, requests
from pathlib import Path

def load_env():
    env = {}
    for line in open(Path.home() / "Desktop/AI経営本部/API連携/.env"):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"')
    return env

def post_to_discord(message, channel_id=None):
    env = load_env()
    token = env.get("DISCORD_BOT_TOKEN", "")
    cid = channel_id or env.get("DISCORD_TIMELINE_CHANNEL_ID", "")
    url = "https://discord.com/api/v10/channels/%%s/messages" %% cid
    headers = {"Authorization": "Bot %%s" %% token, "Content-Type": "application/json"}
    chunks = [message[i:i+1990] for i in range(0, len(message), 1990)]
    for chunk in chunks:
        res = requests.post(url, headers=headers, json={"content": chunk})
        if res.status_code == 200:
            print("✅ Discord投稿成功（%%d文字）" %% len(chunk))
        else:
            print("❌ エラー: %%d %%s" %% (res.status_code, res.text))

if __name__ == "__main__":
    msg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "テスト投稿"
    post_to_discord(msg)
