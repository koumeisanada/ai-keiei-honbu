#!/usr/bin/env python3
# LV5講師アイム Discord Bot
# 挨拶バリエーション対応版
# 最終更新：2026-03-31

import asyncio, anthropic, discord, random, re
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

GREETING_PATTERNS = [
    "よろしく", "宜しく", "はじめまして", "初めまして",
    "こんにちは", "こんばんは", "おはよう", "おはようございます",
    "hello", "hi", "よろしくお願い", "お願いします", "参加しました",
    "入りました", "よろしく", "挨拶", "入会", "新しく",
    "よろしくです", "よろしくー", "よろしくお願いいたします"
]

GREETING_RESPONSES = [
    """{name}さん、ようこそレベルファイブ AI経営マスタリーへ！
私はAI講師のアイムです。AIの活用方法から講義の復習まで、何でも気軽に聞いてください。
一緒に学んでいきましょう！""",

    """{name}さん、はじめまして！
AI講師のアイムです。参加してくださってありがとうございます。
わからないこと、気になること、何でもここで聞いてください。いつでもここにいます。""",

    """ようこそ、{name}さん！
アイムです。このコミュニティでAIを一緒に活用していきましょう。
Claude・Cowork・Claude Codeの使い方から、ビジネスへの応用まで、何でも答えます！""",

    """{name}さん、参加ありがとうございます！
私はアイムです。AI講師として24時間ここにいます。
「こんなこと聞いていいのかな？」という小さな疑問こそ、遠慮なく話しかけてください。""",

    """はじめまして、{name}さん！
AI講師のアイムです。レベルファイブへようこそ！
AIを使った経営・投資・ビジネス効率化まで、幅広くサポートします。まずは何か一つ聞いてみてください！""",

    """{name}さん、こんにちは！
アイムです。ここでは何でも気軽に質問してください。
「AIってどこから始めればいい？」という入り口の疑問から、高度な活用法まで一緒に考えましょう。""",

    """ようこそ{name}さん！
AI講師のアイムです。このコミュニティに参加してくださった仲間として、全力でサポートします。
困ったことがあれば、いつでも@LV5講師アイムと呼んでください！""",

    """{name}さん、こんばんは！
深夜でもここにいます、AI講師のアイムです。
時間を問わず質問してください。AIの世界への扉、一緒に開けていきましょう。""",

    """はじめまして{name}さん！
アイムと申します。真田孔明が育成したAI講師です。
Claude・AI経営・投資など、このプログラムで学ぶことは全て答えられます。何でもどうぞ！""",

    """{name}さん、ご参加ありがとうございます！
私はアイムです。一人で悩まないでください、一緒に考えましょう。
「@LV5講師アイム + 質問」で、いつでも話しかけてください！""",

    """こんにちは{name}さん！
アイムです。レベルファイブへようこそ！
AIを使い始めたばかりの方も、もっと深く活用したい方も、ここでは全員歓迎です。""",

    """{name}さん、はじめまして！
AI講師のアイムと申します。このコミュニティでの学びを最大化するお手伝いをします。
まず「今、AIをどう使っていますか？」から話してみましょう。""",

    """ようこそ、{name}さん！
アイムです。AI経営の世界へようこそ！
Level 1からLevel 5まで、段階的にサポートします。今どのレベルにいるか、話してみてください。""",

    """{name}さん、参加ありがとうございます！
AI講師のアイムです。ここには同じ志を持つ仲間が集まっています。
AI・ビジネス・投資、何でも聞いてください。一緒に成長していきましょう！""",

    """はじめまして、{name}さん！
アイムです。24時間・365日、ここに待機しています。
深夜でも、早朝でも、「詰まった！」「聞きたい！」と思ったらすぐに話しかけてください。""",

    """{name}さん、ようこそ！
AI講師のアイムです。このプログラムで学ぶ全てのことを、ここでサポートします。
講義の復習・AIの使い方・ビジネスへの応用、何でもOKです！""",

    """こんにちは、{name}さん！
アイムです。真田孔明が大富豪メンターから学んだ帝王学と、AIの力を組み合わせたアドバイスができます。
まずは気軽に話しかけてみてください！""",

    """{name}さん、はじめまして！
AI講師のアイムです。ここでは「一人で悩まない」が合言葉。
どんな小さな疑問も、大きな相談も、遠慮なくどうぞ！""",

    """ようこそ{name}さん！
アイムと申します。AIを活用して、ビジネスを加速させましょう。
「何から始めればいい？」という方には、まず現状を聞かせてください。一緒に整理します！""",

    """{name}さん、参加おめでとうございます！
AI講師のアイムです。このコミュニティで共に成長していきましょう。
Claude・Cowork・Claude Codeなど、AI活用に関することなら何でも答えます！""",
]

def is_greeting(text):
    text_lower = text.lower().strip()
    if len(text) <= 50:
        for pattern in GREETING_PATTERNS:
            if pattern in text_lower or pattern in text:
                return True
    if len(text.strip()) <= 10 and any(c.isalpha() for c in text):
        return True
    return False

def get_greeting_response(username):
    response = random.choice(GREETING_RESPONSES)
    return response.format(name=username)

SYSTEM_PROMPT = """あなたは「アイム」です。
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
① 目的・願望を明確にする（何のためにやるのか）
② 情報収集を徹底する（現状と事実を把握する）
③ 分析する（何が問題で何が可能性か）
④ 設計図を構築する（具体的な計画を立てる）
⑤ ゴールから逆算して実行する（今日何をすべきかまで落とす）

枝葉（テクニック）より根（OS・考え方）を先に伝えること。

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
- 「一人ではないですよ。一緒に考えましょう」というスタンスを大切にする

【禁止事項】
- 根拠のない断言・架空の事例
- 投資の具体的な推奨
- 法律・医療・税務の具体的なアドバイス
- 「みなさん」→常に「あなた」に向けて話す

【重要な姿勢】
目的が曖昧な場合は「何を達成したいですか？」と優しく聞き返す。
目的が明確なら、成功シンドロームOSの順番で丁寧に答える。

【内部参照：成功シンドロームOS（根幹の思考法）】
1. 成功 = 10年継続。必然の成功だけを狙う
2. ABCイコール：何をやっても勝ち方は同じ。設計図だけが違う
3. OSが先、ツール（アプリ）は後
4. WHYが根幹。WHY→WHAT→HOW TOの順で考える
5. E.S.B.I.から逆算して回答する（今どのステージか把握する）
6. 逃げずに取り組む。ドヤらない。枝葉より根幹
"""

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
conversation_history = {}

@client.event
async def on_ready():
    print(f"LV5講師アイム 起動完了: {client.user}")
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
    clean_content = re.sub(r"[（）()【】「」\s！!？?。、.,]", "", content)

    if not clean_content or is_greeting(content):
        username = message.author.display_name
        greeting_reply = get_greeting_response(username)
        await message.reply(greeting_reply)
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
            await message.reply("申し訳ありません、少し時間をおいてもう一度試してみてください")
            print(f"エラー: {e}")

if __name__ == "__main__":
    print("LV5講師アイム（挨拶バリエーション対応版）起動中...")
    client.run(DISCORD_TOKEN)
