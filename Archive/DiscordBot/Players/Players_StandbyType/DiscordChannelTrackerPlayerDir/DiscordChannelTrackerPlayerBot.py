import os
from datetime import datetime as dy
import discord
from discord.ext import commands

class DiscordChannelTrackerBot:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.bot = commands.Bot(command_prefix="!")

        # チャンネルが作成されたときに呼び出されるイベントを設定
        @self.bot.event
        async def on_guild_channel_create(channel):
            await self.create_flag_for_channel(channel)

    async def create_flag_for_channel(self, channel):
        # チャンネル用のディレクトリを作成 (存在していなければ)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        channel_dir = os.path.join(base_dir, "channel_flags")
        os.makedirs(channel_dir, exist_ok=True)

        # 現在時刻とチャンネルの名前で .flag ファイルを作成
        flag_file = os.path.join(channel_dir, f"{dy.now().strftime('%Y%m%d_%H%M%S')}_{channel.name}.flag")
        with open(flag_file, 'w') as flag:
            pass  # 空のファイルを作成

        print(f"チャンネル {channel.name} が作成されました。 {flag_file} を作成しました。")

    def run_bot(self):
        self.bot.run(self.bot_token)

# メイン関数でBotを起動
if __name__ == "__main__":
    bot_token = "YOUR_DISCORD_BOT_TOKEN"  # ここにBotのトークンを入力
    channel_tracker_bot = DiscordChannelTrackerBot(bot_token)
    channel_tracker_bot.run_bot()
