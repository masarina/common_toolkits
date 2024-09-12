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
            existing_channel = discord.utils.get(category.channels, name=channel_name)  # 既存のチャンネルをチェック
            if existing_channel:
                print(f"チャンネル '{channel_name}' は既にカテゴリ '{category.name}' に存在しています。")
                return existing_channel.id  # 既存チャンネルのIDを返す
            else:
                new_channel = await guild.create_text_channel(name=channel_name, category=category)  # チャンネルを作成
                print(f"チャンネル '{channel_name}' がカテゴリ '{category.name}' に作成されました。")
                return new_channel.id  # 作成されたチャンネルのIDを返す
        else:
            print(f"カテゴリID {category_id} が見つかりません。")
            return None  # カテゴリが見つからない場合はNoneを返す
    
    
    def main(self):
        """
        メインメソッド。非同期のcreate_channelを実行する。
        """
        
        # 作成するチャンネルについての設定(一度に複数のチャンネルを設定出来ます。)
        # 1つ前のプレイヤーで設定してください
        category_channel_2dList = self.one_time_world_instance.ball.all_data_dict["categoryID_and_channelID_2dList_of_create_Channel"]
        
        
        # チャンネルの作成
        discord_client = self.one_time_world_instance.ball.all_data_dict["bot_instance"]  # botインスタンスを取得
        for category_channel_dict in category_channel_2dList:
            category_id = category_channel[0] # カテゴリIDを取得
            channel_name = category_channel[1] # チャンネル名を取得
            attach_ID = category_channel[2] # チャンネルIDをusers情報として追加するかのbool
            are_you_bot = category_channel[3] # この送信がbotか否かのbool
            
            # チャンネルを作成
            created_channel_id = discord_client.loop.run_until_complete(self.create_channel(category_id, channel_name))  # 非同期メソッドを同期的に実行
            
            # チャンネルが作成されるため、非同期関数チャンネルトラッカーが発動してしまう。
            # チャンネルの確認メッセージ関数が実行されてしまう。
            # チャンネルの確認メッセージ関数の方で、｢確認したチャンネルjson｣を用意する。
            # これはall_data_dictにも更新型で保持させる。
            # そして、ココ作成したチャンネルは、
            # 確認メッセージは発動させてはならないので、
            # 予め{channel_id:"Completed"}として保存する。
            json_path = self.one_time_world_instance.ball.all_data_dict["channel_owner_verified_json_path"]
            with open(json_path, 'r') as json_file:
                channel_owner_verified_dict = json.load(json_file)
            channel_owner_verified_dict.update({str(created_channel_id):"Completed"})
            self.save_data_to_json(channel_owner_verified_dict, json_path)

        # 設定をNoneで初期化
        self.one_time_world_instance.ball.all_data_dict["categoryID_and_channelID_2dList_of_create_Channel"] = None
        
        return "Completed"
        
        
                
    def save_data_to_json(self, data, file_path):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"データが {file_path} に保存されました。")
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
