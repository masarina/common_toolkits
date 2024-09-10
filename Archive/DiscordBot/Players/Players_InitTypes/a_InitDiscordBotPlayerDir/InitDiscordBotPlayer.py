import os, sys
sys.path.append("../..")
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer
import discord

class InitDiscordBotPlayer(SuperPlayer):
    def __init__(self):
        super().__init__()  # スーパークラスの初期化メソッドを呼び出す
        self.my_name = None

    def return_my_name(self):
        return "InitDiscordBotPlayer"

    def main(self):
        """
        Discordのボットをトークンとともに初期化し、ball.all_data_dictに設定するメソッド
        """
        intents = discord.Intents.default()
        intents.messages = True
        intents.guilds = True
        
        # Discordのボットを初期化
        bot = discord.Client(intents=intents)
        
        # トークンを取得
        token = self.one_time_world_instance.ball.all_data_dict["token"]
        
        # ボットをballのall_data_dictに設定
        # botは低レベルの参照渡しによって、他のプレイヤーでもrunされた状態で使用可能
        self.one_time_world_instance.ball.all_data_dict["bot"] = bot
        
        print("Discord bot が初期化され、ball.all_data_dictに設定されました。")
        
        # ボットをトークンで実行（実行後もbotはall_data_dictで他のプレイヤーからアクセス可能）
        bot.run(token)

        return "Completed"
