import os
import subprocess
from datetime import datetime as dt
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class DiscordMemberTrackerPlayer(SuperPlayer):
    """
    DiscordMemberTrackerPlayerクラス
    プレイヤーはBallPassSchedulePatternに従い、Discordのメンバー参加をトラッキングします。
    このプレイヤーはサブプロセスで`DiscordMemberTrackerBot.py`を実行し、新しいメンバーがサーバーに参加したかどうかを管理します。

    Attributes:
        flag_file_name (str): フラグファイル名を保持するための変数。新しいメンバーが参加した際に生成されたフラグファイルの名前を格納します。
    """

    def __init__(self):
        """
        初期化メソッド
        BallPassSchedulePatternに従い、SuperPlayerの初期化メソッドを呼び出します。
        さらに、`DiscordMemberTrackerBot.py`をサブプロセスで実行して、Discordの新しいメンバーを追跡する準備を整えます。
        """
        super().__init__()  # スーパークラスの初期化メソッドを呼び出す
        self.flag_file_name = None  # フラグファイル名を保持するための変数

        # DiscordMemberTrackerBot.pyをサブプロセスで実行
        base_dir = os.path.dirname(os.path.abspath(__file__))  # 現在のファイルのディレクトリを取得
        bot_script = os.path.join(base_dir, "DiscordMemberTrackerBot.py")  # `DiscordMemberTrackerBot.py` の絶対パスを作成

        # サブプロセスで `DiscordMemberTrackerBot.py` を実行し、非同期にDiscordのイベントを監視する
        subprocess.Popen(["python3", bot_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"DiscordMemberTrackerBot.py をサブプロセスで実行しました。")  # デバッグ用のメッセージ

    def return_my_name(self):
        """
        プレイヤーの名前を返すメソッド
        このクラスの名前を返します。BallPassSchedulePatternの一環として使用されます。
        
        Returns:
            str: クラス名 "DiscordMemberTrackerPlayer"
        """
        return "DiscordMemberTrackerPlayer"

    def main(self):
        """
        メイン処理
        フラグファイルを確認し、存在すれば`self.one_time_world_instance.ball.all_data_dict`にフラグを立てます。
        フラグファイルが存在する場合、削除してファイル名の保持を解除します。
        この処理はBallPassSchedulePatternの流れに沿って、ワールド内でのプレイヤー間のキャッチボールの一環として行われます。

        Returns:
            str: 完了メッセージ "Completed"
        """
        # フラグファイルを探すディレクトリ
        base_dir = os.path.dirname(os.path.abspath(__file__))  # 現在のファイルのディレクトリを取得
        member_dir = os.path.join(base_dir, "flags")  # フラグファイルのディレクトリパスを生成

        # フラグファイルの存在をチェック
        if os.path.exists(member_dir):
            for file_name in os.listdir(member_dir):
                if file_name.endswith(".flag"):
                    self.flag_file_name = file_name  # フラグファイル名を保持
                    # フラグファイルが存在していたら `all_data_dict` にフラグを設定
                    self.one_time_world_instance.ball.all_data_dict["newUser_flag"] = True

                    # フラグファイルを削除し、ファイル名の保持を解除
                    os.remove(os.path.join(member_dir, self.flag_file_name))
                    self.flag_file_name = None  # フラグファイル名をリセット
                    print(f"フラグファイル {file_name} を削除しました。")  # デバッグ用メッセージ

        return "Completed"
