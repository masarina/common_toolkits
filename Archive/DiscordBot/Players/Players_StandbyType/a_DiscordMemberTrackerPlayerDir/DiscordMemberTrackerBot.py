import os
from datetime import datetime as dy
import discord
from discord.ext import commands

class DiscordMemberTrackerBot:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.bot = commands.Bot(command_prefix="!")

        # メンバーがサーバーに参加したときに呼び出されるイベントを設定
        @self.bot.event
        async def on_member_join(member):
            await self.create_flag_for_new_member(member)

    async def create_flag_for_new_member(self, member):
        # メンバー用のディレクトリを作成 (存在していなければ)
        member_dir = "./flags"
        os.makedirs(member_dir, exist_ok=True)

        # 現在時刻の .flag ファイルを作成 (追加型)
        flag_file = os.path.join(member_dir, f"{dy.now().strftime('%Y%m%d_%H%M%S')}.flag")
        with open(flag_file, 'w') as flag:
            pass  # 空のファイルを作成

        print(f"{member.name} がサーバーに参加しました。 {flag_file} を作成しました。")

    def run_bot(self):
        self.bot.run(self.bot_token)

# メイン関数でBotを起動
if __name__ == "__main__":
    bot_token = "YOUR_DISCORD_BOT_TOKEN"  # ここにBotのトークンを入力
    tracker_bot = DiscordMemberTrackerBot(bot_token)
    tracker_bot.run_bot()
