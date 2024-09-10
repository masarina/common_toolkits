import os
import asyncio
from discord.ext import commands
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class WelcomeNewUserPlayer(SuperPlayer):
    def __init__(self):
        super().__init__()
        self.my_name = None

    def return_my_name(self):
        return "WelcomeNewUserPlayer"

    def main(self):
        """
        visitorとしてマークされているユーザーに
        ハローメッセージを送信、visitorユーザ専用チャンネルの作成、
        その後にユーザーランクを
        'new_user'にアップグレードします。
        """
        # user情報の辞書を取得
        user_info_pickle_path = self.one_time_world_instance.ball.all_data_dict.get("all_user_information_dict")

        # pickleファイルからデータを読み込む
        user_data = self.load_data_from_pickle(user_info_pickle_path)

        # visitorのランクを持つユーザーを取得
        visitor_ids = [user_id for user_id, data in user_data.items() if data["user_rank"] == "visitor"]

        if not visitor_ids:
            print("visitorランクのユーザーが見つかりませんでした。")
            return "No visitors"

        # 最初のvisitorを対象にする
        target_user_id = visitor_ids[0]

        # bot、channel_id、messageを取得
        bot = self.one_time_world_instance.ball.all_data_dict.get("bot_instance")
        channel_id = self.one_time_world_instance.ball.all_data_dict.get("hello_message_channel_id")
        welcome_message = f"Hello, {target_user_id}! Welcome to the server!"

        # 必要なデータが取得できなかった場合のエラーチェック
        if not bot or not channel_id or not welcome_message:
            raise ValueError("必要なデータがball.all_data_dictから取得できませんでした。")

        # ハローメッセージを送信
        asyncio.run(one_time_world_instance.sendMessagePlayer.send_message(bot, channel_id, welcome_message))

        # 次のプレイヤーでvisitorさん専用のチャンネルを作成してあげるので、その設定。
        visitorUser_name = (await bot.fetch_user(target_user_id)).name
        self.one_time_world_instance.ball.all_data_dict["categoryID_and_channelID_dict_of_create_Channel"] = [
            [1195503636453793792,f"{visitorUser_name}さん_作業場"],
            [1195503636453793792, f"{visitorUser_name}さん_休憩場"]
        ] # 作成するチャンネルを[カテゴリID,チャンネル名]
        

        # ランクをnew_userにアップグレード
        user_data[target_user_id]["user_rank"] = "new_user"

        # データをpickleに保存
        self.save_data_to_pickle(user_data, user_info_pickle_path)


        print(f"{target_user_id}のランクをnew_userにアップグレードしました。")
        return "Completed"

    def load_data_from_pickle(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        else:
            return {}

    def save_data_to_pickle(self, data, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
        print(f"データが {file_path} に保存されました。")