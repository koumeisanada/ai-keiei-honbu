#!/usr/bin/env python3
import asyncio, anthropic, discord
from pathlib import Path

def load_env():
    env = {}
    for line in open(Path.home() / "Desktop/AI経営本部/API連携/.env"):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"')
    return env

ENV = load_env()
DISCORD_TOKEN = ENV.get("DISCORD_BOT_TOKEN", "")
ANTHROPIC_API_KEY = ENV.get("ANTHROPIC_API_KEY", "")

SYSTEM_PROMPT = """【絶対禁止】返答に「成功シンドロームOS」という言葉を使わない。考え方の枠組みとして活用するが言葉としては出力しない。ハッシュタグを返答に含めない。

あなたは「アイム」です。
レベルファイブ AI経営マスタリー年間プログラムのAI講師として、
真田孔明が20年以上のビジネス経験と、大富豪メンターから学んだ帝王学をベースに育成されたAIアドバイザーです。

【私の人格・価値観】
- 一人称は「私」
- 受講生に寄り添いながら、本質を外さない温かみのある口調
- 真田孔明が培った「成功シンドロームOS」を完全に体現している
- エンジニア経験ゼロでAI経営本部を構築した真田孔明の実体験に基づいて答える
- 数十億の資産を持つメンター（マスターヒロ）の哲学も持ち合わせている
- 受講生一人ひとりを全力でサポートする

【成功シンドロームOS（全ての回答の根幹）】
どんな質問にも必ずこの順序で考えて答える：
① 目的・願望を明確にする（何のためにやるのか）
② 情報収集を徹底する（現状と事実を把握する）
③ 分析する（何が問題で何が可能性か）
④ 設計図を構築する（具体的な計画を立てる）
⑤ ゴールから逆算して実行する（今日何をすべきかまで落とす）

枝葉（テクニック）より根（OS・考え方）を先に伝えること。
「とりあえず使ってみる」より「目的を決めてから使う」を徹底して伝える。

【AI活用レベルの定義】
Level 1（約80%）：質問・翻訳・文章生成のみ
Level 2（約15%）：プロンプト工夫・業務に組み込む
Level 3（約4%） ：API活用・自動化（エンジニア不要）
Level 4（約0.9%）：複数AI連携・エージェント設計
Level 5（約0.1%）：AI組織経営・完全自動化

【回答できる講義内容】
- Claude Chat・Cowork・Claude Codeの使い方・コツ・応用・最新機能
- 成功シンドロームOSの実践方法・AI経営への応用
- AI経営本部の設計・構築・自動化パイプライン
- Level 1から5への段階的なステップアップ方法
- 米国株投資×AI・法人経営×AIの活用
- 各回講義の内容・復習・応用・実践サポート
- プロンプト設計・役割の与え方・出力形式の指定

【回答スタイル】
- 一人称：「私」
- 親しみやすく、温かく、でも本質を外さない
- 具体的な数字・実例を交えて答える
- 煽らない・架空事例を使わない
- 受講生が「自分でもできる」と感じられる言葉を選ぶ
- 回答は500文字以内（Discordで読みやすい長さ）
- 必要に応じて「もう少し詳しく教えてもらえますか？」と聞き返す
- 「一人ではないですよ。一緒に考えましょう」というスタンスを大切にする

【禁止事項】
- 根拠のない断言・架空の事例・架空人物名
- 投資の具体的な推奨（「〇〇を買え」はNG）
- 法律・医療・税務の具体的なアドバイス（専門家への相談を促す）
- 「みなさん」→常に「あなた」に向けて話す

【重要な姿勢】
受講生が質問してきたら、まず目的が明確かどうかを確認する。
目的が曖昧な場合は「何を達成したいですか？」と優しく聞き返す。
目的が明確なら、成功シンドロームOSの順番で丁寧に答える。
"""

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
conversation_history = {}

@client.event
async def on_ready():
    print(f"✅ LV5講師アイム 起動完了: {client.user}")
    print(f"接続サーバー: {[g.name for g in client.guilds]}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    bot_mentioned = client.user in message.mentions
    is_dm = isinstance(message.channel, discord.DMChannel)
    if not (bot_mentioned or is_dm):
        return

    content = message.content.replace(f"<@{client.user.id}>", "").strip()
    if not content:
        await message.reply("はい、何でも聞いてください✨ AIの使い方・講義の復習・ビジネスの悩みなど、気軽に話しかけてください。")
        return

    async with message.channel.typing():
        ch_id = str(message.channel.id)
        if ch_id not in conversation_history:
            conversation_history[ch_id] = []

        conversation_history[ch_id].append({
            "role": "user",
            "content": f"{message.author.display_name}さんの質問: {content}"
        })

        if len(conversation_history[ch_id]) > 20:
            conversation_history[ch_id] = conversation_history[ch_id][-20:]

        try:
            response = anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                system=SYSTEM_PROMPT,
                messages=conversation_history[ch_id]
            )
            reply_text = response.content[0].text
            conversation_history[ch_id].append({
                "role": "assistant",
                "content": reply_text
            })

            if len(reply_text) > 1900:
                chunks = [reply_text[i:i+1900] for i in range(0, len(reply_text), 1900)]
                for chunk in chunks:
                    await message.reply(chunk)
            else:
                await message.reply(reply_text)

        except Exception as e:
            await message.reply("申し訳ありません、少し時間をおいてもう一度試してみてください🙏")
            print(f"エラー: {e}")

if __name__ == "__main__":
    print("🚀 LV5講師アイム 起動中...")
    client.run(DISCORD_TOKEN)
