import json
import discord
from discord.ext import commands

class DiscordMemberTrackerBot:
    def __init__(self, bot_token, json_file):
        self.bot_token = bot_token
        self.json_file = json_file
        self.bot = commands.Bot(command_prefix="!")

        # メンバーがサーバーに参加したときに呼び出されるイベントを設定
        @self.bot.event
        async def on_member_join(member):
            await self.update_json_file_with_new_member(member)

    async def update_json_file_with_new_member(self, member):
        # JSONファイルのデータを読み込み、更新して保存
        try:
            with open(self.json_file, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}  # ファイルがない場合は新しく作る

        # メンバーのIDをキーに、Trueに更新
        data["joined"] = True

        # 更新した内容をJSONファイルに書き込む
        with open(self.json_file, 'w') as file:
            json.dump(data, file, indent=4)

        print(f"{member.name}がサーバーに参加しました。JSONファイルを更新しました。")

    def run_bot(self):
        self.bot.run(self.bot_token)

# メイン関数でBotを起動
if __name__ == "__main__":
    bot_token = "YOUR_DISCORD_BOT_TOKEN"  # ここにBotのトークンを入力
    json_file = "member_data.json"  # JSONファイルの名前

    tracker_bot = DiscordMemberTrackerBot(bot_token, json_file)
    tracker_bot.run_bot()
