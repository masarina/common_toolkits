import os
import asyncio
from discord.ext import commands
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class SendMessagePlayer(SuperPlayer):
    def __init__(self):
        super().__init__()  # スーパークラスの初期化メソッドを呼び出す
        self.my_name = None

    def return_my_name(self):
        return "SendMessagePlayer"

    def main(self):
        """
        SuperPlayerのメンバ変数。
        このmainメソッドは同期関数として実行されるが、
        bot、channel_id、messageをball.all_data_dictから取得し、
        非同期処理を行います。
        """

        # ballからbotインスタンス、チャンネルID、メッセージを取得
        bot = self.one_time_world_instance.ball.all_data_dict.get("send_message_player_bot_instance")
        ChID_MESSE_2dList = self.one_time_world_instance.ball.all_data_dict.get("sendMessage_2dList_CHANNELID_MESSE")
         
        # 必要なデータが取得できなかった場合のエラーチェック
        if not bot or not ChID_MESSE_2dList:
            raise ValueError("必要なデータがball.all_data_dictから取得できませんでした。")

        # 非同期処理を実行してメッセージを送信
        for pair in ChID_MESSE_2dList:
            channel_id = pair[0]
            message = pair[1]
            asyncio.run(self.send_message(bot, channel_id, message))

        return "Completed"

    async def send_message(self, bot, channel_id, message):
        """
        指定されたチャンネルにメッセージを送信する非同期関数。
        """
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(message)
        else:
            print(f"チャンネルID {channel_id} が見つかりませんでした。")
