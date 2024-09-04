import json
import os
import discord
from discord.ext import commands

class ChannelActivityTracker:
    """
    新しいチャンネルが作成されたときに、チャンネルIDと
    その時に活動していたユーザーIDをJSONファイルに保存するクラス。
    """
    
    def __init__(self, json_file_path):
        # JSONファイルのパスを設定
        self.json_file_path = json_file_path
        # Discord Botを初期化
        self.bot = commands.Bot(command_prefix="!")

    def load_json_data(self):
        """
        JSONファイルからデータを読み込む。
        ファイルが存在しない場合は、空の辞書を返すよ。
        """
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'r') as file:
                return json.load(file)
        else:
            return {}

    def save_json_data(self, data):
        """
        更新されたデータをJSONファイルに保存する。
        インデントをつけて、読みやすく整形しておくよ。
        """
        with open(self.json_file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def remove_duplicates(self, user_ids):
        """
        ユーザーIDのリストから重複するIDを削除して、ユニークなリストを返す。
        """
        return list(set(user_ids))

    async def on_guild_channel_create(self, channel):
        """
        新しいチャンネルが作成されたときに呼び出されるイベントハンドラ。
        チャンネルIDと活動していたユーザーのIDを取得して、JSONファイルに保存するよ。
        """
        # チャンネルIDを取得
        channel_id = channel.id

        # チャンネル作成時に活動していたユーザーIDを取得
        active_user_ids = []
        async for entry in channel.guild.audit_logs(limit=10, action=discord.AuditLogAction.channel_create):
            active_user_ids.append(entry.user.id)

        # JSONデータを読み込み
        data = self.load_json_data()

        # 新しいチャンネルIDがまだデータにない場合、リストを作成
        if channel_id not in data:
            data[channel_id] = []

        # 新しいユーザーIDをリストに追加
        data[channel_id].extend(active_user_ids)

        # 重複するユーザーIDを削除
        data[channel_id] = self.remove_duplicates(data[channel_id])

        # 更新されたデータをJSONファイルに保存
        self.save_json_data(data)

        print(f"新しいチャンネル {channel_id} が作成されました。活動していたユーザー: {active_user_ids} を保存しました。")

    def run_bot(self, token):
        """
        Botを起動して、チャンネル作成イベントの監視を開始する。
        """
        # イベントハンドラを登録
        @self.bot.event
        async def on_guild_channel_create(channel):
            await self.on_guild_channel_create(channel)

        # Botを実行
        self.bot.run(token)

def main():
    """
    メイン関数として、サブプロセスで実行可能。
    Botを起動してチャンネルアクティビティトラッカーを開始する。
    """
    # JSONファイルのパスを設定
    json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "channel_user_data.json")
    
    # Botのトークンを設定(安全のため、環境変数から取得することを推奨)
    bot_token = 'YOUR_BOT_TOKEN'

    # チャンネルアクティビティトラッカーのインスタンスを作成
    tracker = ChannelActivityTracker(json_file_path)
    
    # Botを起動してチャンネル監視を開始
    tracker.run_bot(bot_token)

# メイン関数を実行
if __name__ == "__main__":
    main()