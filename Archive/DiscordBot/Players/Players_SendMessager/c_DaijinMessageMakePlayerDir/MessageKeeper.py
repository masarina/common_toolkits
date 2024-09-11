import os
import json
from discord.ext import commands
from datetime import datetime

class MessageKeeper:
    def __init__(self):
        # 辞書の初期化
        self.messages_dict = {}
        # JSONファイルのパスを設定
        self.json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'messages.json')
        
        # Botの設定
        self.bot = commands.Bot(command_prefix="!")

    def on_ready(self):
        print(f'Bot is ready and running as {self.bot.user}')

    def on_message(self, message):
        # メッセージがBot自身からのものなら無視
        if message.author == self.bot.user:
            return
        
        # 日付時刻を取得
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # ユーザーID、チャンネルID、メッセージ内容を辞書に追加
        self.messages_dict[timestamp] = {
            "user_id": message.author.id,
            "channel_id": message.channel.id,
            "message": message.content
        }

        # JSONファイルに追記して保存
        self.save_to_json()

    def save_to_json(self):
        # 既存のデータを読み込む
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'r') as json_file:
                try:
                    existing_data = json.load(json_file)
                except json.JSONDecodeError:
                    existing_data = {}
        else:
            existing_data = {}

        # 新しいデータを既存のデータに追加
        existing_data.update(self.messages_dict)

        # データをJSONファイルに保存
        with open(self.json_file_path, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)
        
        print(f"データが {self.json_file_path} に保存されました。")

    def main(self):
        # Botを同期的に実行
        self.bot.event(self.on_ready)
        self.bot.event(self.on_message)
        self.bot.run("YOUR_BOT_TOKEN")  # Botのトークンを入れてください

if __name__ == "__main__":
    keeper = MessageKeeper()
    keeper.main()
