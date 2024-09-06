import os
from datetime import datetime as dy
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class DiscordMemberTrackerPlayer(SuperPlayer):
    def __init__(self):
        super().__init__()  # スーパークラスの初期化メソッドを呼び出す
        self.flag_file_name = None

    def return_my_name(self):
        return "DiscordMemberTrackerPlayer"

    def main(self):
        # フラグファイルを探すディレクトリ
        member_dir = "./flags"

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
