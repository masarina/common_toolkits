import os, sys
sys.path.append("../..")
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer 
import discord

class CreateChannelPlayer(SuperPlayer):
    def __init__(self):
        super().__init__()  # スーパークラスの初期化メソッドを呼び出す
        self.my_name = None

    def return_my_name(self):
        return "CreateChannelPlayer"

    async def create_channel(self, category_id, channel_name):
        """
        チャンネルを作成する非同期メソッド。
        category_id: 作成するカテゴリのID
        channel_name: 作成するチャンネル名
        """
        guild = self.one_time_world_instance.ball.all_data_dict["bot_instance"].guilds[0]  # サーバーを取得
        category = discord.utils.get(guild.categories, id=category_id)  # カテゴリを取得
        if category:
            await guild.create_text_channel(name=channel_name, category=category)  # チャンネルを作成
        else:
            print(f"カテゴリID {category_id} が見つかりません。")

    def main(self):
        """
        メインメソッド。非同期のcreate_channelを実行する。
        """
        category_id = self.one_time_world_instance.ball.all_data_dict["category_id"]  # カテゴリIDを取得
        channel_name = self.one_time_world_instance.ball.all_data_dict["channel_name"]  # チャンネル名を取得
        discord_client = self.one_time_world_instance.ball.all_data_dict["bot_instance"]  # botインスタンスを取得
        
        discord_client.loop.run_until_complete(self.create_channel(category_id, channel_name))  # 非同期メソッドを同期的に実行

        return "Completed"
