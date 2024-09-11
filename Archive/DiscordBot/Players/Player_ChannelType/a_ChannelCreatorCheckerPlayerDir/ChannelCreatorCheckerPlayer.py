import json
import os
import discord
import asyncio
from discord.ext import commands

class ChannelCreatorCheckerPlayer(SuperPlayer):
    def __init__(self):
        super().__init__()
        self.my_name = "ChannelCreatorCheckerPlayer"
        self.channel_creator_data_path = f"{os.path.dirname(os.path.abspath(__file__))}/channel_user_data.json"
        self.channel_creator_info_json_path = f"{os.path.dirname(os.path.abspath(__file__))}/channel_creator_info.json"

    def return_my_name(self):
        return self.my_name

    def run(self, discord_bot):
        """
        メイン関数内で呼び出す、非同期処理のラッパー関数。
        """
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.check_channel_creator(discord_bot))
        return result

    async def check_channel_creator(self, discord_bot):
        """
        チャンネル作成者を確認するメソッド。
        チャンネル内でyes/noを聞いて、どのユーザーでも応答を受け付ける。
        作成者が分かった場合は、そのユーザーIDとチャンネルIDを返す。
        """
        # チャンネルデータが保存されているJSONファイルのパス
        channel_data_json_path = self.channel_creator_data_path
        if not os.path.exists(channel_data_json_path):
            return None

        with open(channel_data_json_path, 'r') as file:
            channel_data = json.load(file)

        # チャンネルIDを取得（最初のチャンネルを例として取得）
        if not channel_data:
            return None
        target_channel_id = next(iter(channel_data))  # JSONの最初のチャンネルIDを取得

        # チャンネルオブジェクトを取得
        target_channel = discord_bot.get_channel(int(target_channel_id))

        # ユーザーIDのリストを取得
        active_user_ids = channel_data[target_channel_id]

        # チャンネル作成者を確認する
        for user_id in active_user_ids:
            active_user = discord_bot.get_user(int(user_id))
            if active_user is None:
                continue

            # チャンネルでユーザーにメッセージを送信して確認する
            await target_channel.send(f"このチャンネルの作成者は{active_user.name}さんですか？ yes/no")

            def check_message_response(message):
                return message.channel.id == target_channel.id and message.content.lower() in ['yes', 'no', 'y', 'n']

            try:
                # メッセージの返答を待つ（どのユーザーでもOK）
                response_message = await discord_bot.wait_for('message', check=check_message_response)
                if response_message.content.lower() in ['yes', 'y']:
                    # 作成者が確認された場合、ユーザーIDとチャンネルIDを返す
                    return user_id, target_channel_id
                elif response_message.content.lower() in ['no', 'n']:
                    continue
            except:
                continue

        # 作成者が見つからなかった場合はNoneを返す
        return None

    def update_channel_creator_info(self, creator_user_id, created_channel_id):
        """
        チャンネル作成者の情報を新しいJSONファイルに更新するメソッド。
        """
        channel_creator_info_json_path = self.channel_creator_info_json_path

        # 既存のデータを読み込み、無ければ新しく作成
        if os.path.exists(channel_creator_info_json_path):
            with open(channel_creator_info_json_path, 'r') as file:
                channel_creator_info = json.load(file)
        else:
            channel_creator_info = {}

        # チャンネルIDと作成者のユーザーIDを追加・更新
        channel_creator_info[creator_user_id] = created_channel_id

        # 更新されたデータを保存
        with open(channel_creator_info_json_path, 'w') as file:
            json.dump(channel_creator_info, file, indent=4)

    def main(self):
        """
        チャンネル作成者を確認して処理するメイン関数。
        """
        # 必要な情報を取得
        discord_bot = self.one_time_world_instance.ball.all_data_dict["bot"]

        # チャンネルデータが保存されているJSONファイルのパス
        channel_data_json_path = f"{os.path.dirname(os.path.abspath(__file__))}/channel_user_data.json"
        while os.path.exists(channel_data_json_path):
            with open(channel_data_json_path, 'r') as file:
                channel_data = json.load(file)
                if not channel_data:
                    break  # JSONにチャンネルIDが無ければループを終了

            # チャンネル作成者を確認するためにrunを呼び出し
            creator_info = self.run(discord_bot)

            # 作成者が確認できた場合、新しいJSONファイルに保存
            if creator_info:
                creator_user_id, created_channel_id = creator_info
                self.update_channel_creator_info(creator_user_id, created_channel_id)

            # 処理が完了したら、元のJSONファイルからチャンネルIDを削除
            if creator_info:
                created_channel_id = next(iter(channel_data))  # JSONの最初のチャンネルIDを取得
                self.remove_channel_from_json(created_channel_id)

        return "Completed"
