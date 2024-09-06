import os
from datetime import datetime as dy
import discord
from discord.ext import commands

class DiscordMessageTrackerBot:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.bot = commands.Bot(command_prefix="!")

        # メッセージが送信されたときに呼び出されるイベントを設定
        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return  # Bot自身のメッセージは無視する

            await self.create_flag_for_message(message)

    async def create_flag_for_message(self, message):
        # メッセージ用のディレクトリを作成 (存在していなければ)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        message_dir = os.path.join(base_dir, "message_flags")
        os.makedirs(message_dir, exist_ok=True)

        # 現在時刻とメッセージの送信者名で .flag ファイルを作成
        flag_file = os.path.join(message_dir, f"{dy.now().strftime('%Y%m%d_%H%M%S')}_{message.author.name}.flag")
        with open(flag_file, 'w') as flag:
            pass  # 空のファイルを作成

        print(f"{message.author.name} がメッセージを送信しました。 {flag_file} を作成しました。")

    def run_bot(self):
        self.bot.run(self.bot_token)

# メイン関数でBotを起動
if __name__ == "__main__":
    bot_token = "YOUR_DISCORD_BOT_TOKEN"  # ここにBotのトークンを入力
    message_tracker_bot = DiscordMessageTrackerBot(bot_token)
    message_tracker_bot.run_bot()
