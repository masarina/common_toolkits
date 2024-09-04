import json
import os
import discord
from discord.ext import commands

class ChannelCreatorCheckerPlayer(SuperPlayer):
    def __init__(self):
        super().__init__()
        self.my_name = "ChannelCreatorCheckerPlayer"

    def return_my_name(self):
        return self.my_name

    async def check_channel_creator(self, bot, channel_id, user_ids):
        """
        チャンネル作成者を確認するメソッド。
        チャンネル内でyes/noを聞いて、どのユーザーでも応答を受け付ける。
        """
        # JSONファイルをロード
        json_file_path = f"{os.path.dirname(os.path.abspath(__file__))}/channel_user_data.json"
        if not os.path.exists(json_file_path):
            return False

        with open(json_file_path, 'r') as file:
            data = json.load(file)

        if channel_id not in data:
            return False

        # チャンネルオブジェクトを取得
        channel = bot.get_channel(channel_id)

        # ユーザーIDのリストを取得
        user_ids = data[channel_id]

        # チャンネル作成者を確認する
        for user_id in user_ids:
            user = bot.get_user(user_id)
            if user is None:
                continue

            # チャンネルでユーザーにメッセージを送信して確認する
            await channel.send(f"このチャンネルの作成者は{user.name}さんですか？ yes/no")

            def check(message):
                return message.channel.id == channel_id and message.content.lower() in ['yes', 'no', 'y', 'n']

            try:
                # メッセージの返答を待つ（どのユーザーでもOK）
                msg = await bot.wait_for('message', check=check)
                if msg.content.lower() in ['yes', 'y']:
                    return True
                elif msg.content.lower() in ['no', 'n']:
                    continue
            except:
                continue

        # 作成者が見つからなかった場合の処理
        await channel.send("ごめんなさい、このチャンネルの作成者を特定できませんでした。お手数ですが、新しくチャンネル作成をお願いします。このチャンネルを削除しますか？ yes/no")

        def delete_check(message):
            return message.channel.id == channel_id and message.content.lower() in ['yes', 'no', 'y', 'n']

        try:
            delete_msg = await bot.wait_for('message', check=delete_check)
            if delete_msg.content.lower() in ['yes', 'y']:
                # チャンネルを削除
                await channel.delete()
                return True
        except:
            pass

        return False

    async def main(self):
        """
        チャンネル作成者を確認して処理するメイン関数。
        """
        # 必要な情報を取得
        bot = self.one_time_world_instance.ball.all_data_dict["bot"]
        channel_id = self.one_time_world_instance.ball.all_data_dict["channel_id"]

        # チャンネル作成者を確認
        result = await self.check_channel_creator(bot, channel_id, [])

        return "Completed" if result else "Failed"
