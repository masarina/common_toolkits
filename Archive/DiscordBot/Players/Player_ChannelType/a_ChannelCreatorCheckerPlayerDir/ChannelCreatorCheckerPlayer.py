import json
import os
import discord
import asyncio
from discord.ext import commands

class ChannelCreatorCheckerPlayer(SuperPlayer):
    def __init__(self):
        super().__init__()
        self.my_name = "ChannelCreatorCheckerPlayer"

    def return_my_name(self):
        return self.my_name

    def run(self, bot):
        """
        メイン関数内で呼び出す、非同期処理のラッパー関数。
        """
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.check_channel_creator(bot))
        return result

    async def check_channel_creator(self, bot):
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

        # チャンネルIDを取得（最初のチャンネルを例として取得）
        if not data:
            return False
        channel_id = next(iter(data))  # JSONの最初のチャンネルIDを取得

        # チャンネルオブジェクトを取得
        channel = bot.get_channel(int(channel_id))

        # ユーザーIDのリストを取得
        user_ids = data[channel_id]

        # チャンネル作成者を確認する
        for user_id in user_ids:
            user = bot.get_user(int(user_id))
            if user is None:
                continue

            # チャンネルでユーザーにメッセージを送信して確認する
            await channel.send(f"このチャンネルの作成者は{user.name}さんですか？ yes/no")

            def check(message):
                return message.channel.id == channel.id and message.content.lower() in ['yes', 'no', 'y', 'n']

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
            return message.channel.id == channel.id and message.content.lower() in ['yes', 'no', 'y', 'n']

        try:
            delete_msg = await bot.wait_for('message', check=delete_check)
            if delete_msg.content.lower() in ['yes', 'y']:
                # チャンネルを削除
                await channel.delete()
                return True
        except:
            pass

        return False

    def remove_channel_from_json(self, channel_id):
        """
        チャンネルIDと対応するユーザーIDリストをJSONファイルから削除するメソッド。
        """
        json_file_path = f"{os.path.dirname(os.path.abspath(__file__))}/channel_user_data.json"
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as file:
                data = json.load(file)

            if channel_id in data:
                del data[channel_id]

            # 更新されたデータをJSONファイルに保存
            with open(json_file_path, 'w') as file:
                json.dump(data, file, indent=4)

    def main(self):
        """
        チャンネル作成者を確認して処理するメイン関数（非同期ではない）。
        """
        # 必要な情報を取得
        bot = self.one_time_world_instance.ball.all_data_dict["bot"]

        # チャンネル作成者を確認するためにrunを呼び出し
        result = self.run(bot)

        # 処理が完了したら、JSONファイルからチャンネルIDを削除
        if result:
            json_file_path = f"{os.path.dirname(os.path.abspath(__file__))}/channel_user_data.json"
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r') as file:
                    data = json.load(file)
                    channel_id = next(iter(data))  # JSONの最初のチャンネルIDを取得
                    self.remove_channel_from_json(channel_id)

        return "Completed" if result else "Failed"
