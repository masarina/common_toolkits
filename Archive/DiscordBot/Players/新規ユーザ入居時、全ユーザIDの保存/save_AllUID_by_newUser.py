import os
import discord
import pickle
from discord.ext import commands

# Botの初期化
bot = commands.Bot(command_prefix="!")

# pickleファイルのパスを設定
file_path = f"{os.path.dirname(os.path.abspath(__file__))}/user_data.pkl"

# ユーザーIDを保存する辞書を初期化
user_data = {"user_ids": []}

def load_data_from_pickle():
    """
    pickleファイルからデータを読み込む関数。
    ファイルが存在しない場合は空の辞書を返す。
    """
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    else:
        return {"user_ids": []}

def save_data_to_pickle(data):
    """
    データをpickleファイルに保存する関数。
    """
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)
    print(f"データが {file_path} に保存されました。")

@bot.event
async def on_member_join(member):
    """
    新しいメンバーがサーバーに参加したときに呼び出されるイベント。
    サーバー内の全ユーザーIDを取得し、辞書に保存、pickleに出力する。
    """
    # サーバー（ギルド）を取得
    guild = member.guild
    
    # 辞書データを更新
    user_data = load_data_from_pickle()
    for member in guild.members:
        user_id_str = str(member.id)
        if user_id_str not in user_data["user_ids"]:
            user_data["user_ids"].append(user_id_str)
    
    # 辞書データをpickleファイルに保存
    save_data_to_pickle(user_data)

    print(f"新しいメンバー {member.name} が参加しました。ユーザーIDを更新しました。")

# Botの実行
bot.run('YOUR_DISCORD_TOKEN')
