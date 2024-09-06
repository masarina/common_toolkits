import os
import subprocess
from datetime import datetime as dt
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class DiscordMemberTrackerPlayer(SuperPlayer):
    def __init__(self):
        super().__init__()  # スーパークラスの初期化メソッドを呼び出す
        self.flag_file_name = None

        # DiscordMemberTrackerBot.pyをサブプロセスで実行する
        base_dir = os.path.dirname(os.path.abspath(__file__))
        bot_script = os.path.join(base_dir, "DiscordMemberTrackerBot.py")

        # サブプロセスで実行
        subprocess.Popen(["python3", bot_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"DiscordMemberTrackerBot.py をサブプロセスで実行しました。")

    def return_my_name(self):
        return "DiscordMemberTrackerPlayer"

    def main(self):
        # フラグファイルを探すディレクトリ
        base_dir = os.path.dirname(os.path.abspath(__file__))
        member_dir = os.path.join(base_dir, "flags")

        # ディレクトリ内のフラグファイルをチェック
        if os.path.exists(member_dir):
            for file_name in os.listdir(member_dir):
                if file_name.endswith(".flag"):
                    self.flag_file_name = file_name
                    # フラグファイルが存在していたらall_data_dictにフラグを立てる
                    self.one_time_world_instance.ball.all_data_dict["newUser_flag"] = True

                    # フラグファイルを削除し、ファイル名の保持を解除
                    os.remove(os.path.join(member_dir, self.flag_file_name))
                    self.flag_file_name = None
                    print(f"フラグファイル {file_name} を削除しました。")

        return "Completed"
