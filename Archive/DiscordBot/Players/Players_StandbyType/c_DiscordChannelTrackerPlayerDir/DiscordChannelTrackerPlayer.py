import os
import subprocess
from datetime import datetime as dt
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class DiscordChannelTrackerPlayer(SuperPlayer):
    """
    DiscordChannelTrackerPlayerクラス
    プレイヤーはBallPassSchedulePatternに従い、Discordのチャンネル作成をトラッキングします。
    このプレイヤーはサブプロセスで`DiscordChannelTrackerBot.py`を実行し、新しいチャンネルが作成されたかどうかを管理します。

    Attributes:
        flag_file_name (str): フラグファイル名を保持するための変数。新しいチャンネルが作成された際に生成されたフラグファイルの名前を格納します。
    """

    def __init__(self):
        """
        初期化メソッド
        BallPassSchedulePatternに従い、SuperPlayerの初期化メソッドを呼び出します。
        さらに、`DiscordChannelTrackerBot.py`をサブプロセスで実行して、Discordの新しいチャンネルを追跡する準備を整えます。
        """
        super().__init__()  # スーパークラスの初期化メソッドを呼び出す
        self.flag_file_name = None  # フラグファイル名を保持するための変数

        # DiscordChannelTrackerBot.pyをサブプロセスで実行
        base_dir = os.path.dirname(os.path.abspath(__file__))  # 現在のファイルのディレクトリを取得
        bot_script = os.path.join(base_dir, "DiscordChannelTrackerBot.py")  # `DiscordChannelTrackerBot.py` の絶対パスを作成

        # サブプロセスで `DiscordChannelTrackerBot.py` を実行し、非同期にDiscordのイベントを監視する
        subprocess.Popen(["python3", bot_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"DiscordChannelTrackerBot.py をサブプロセスで実行しました。")  # デバッグ用のメッセージ

    def return_my_name(self):
        """
        プレイヤーの名前を返すメソッド
        このクラスの名前を返します。BallPassSchedulePatternの一環として使用されます。
        
        Returns:
            str: クラス名 "DiscordChannelTrackerPlayer"
        """
        return "DiscordChannelTrackerPlayer"

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
        channel_dir = os.path.join(base_dir, "channel_flags")  # フラグファイルのディレクトリパスを生成

        # フラグファイルの存在をチェック
        if os.path.exists(channel_dir):
            for file_name in os.listdir(channel_dir):
                if file_name.endswith(".flag"):
                    self.flag_file_name = file_name  # フラグファイル名を保持
                    # フラグファイルが存在していたら `all_data_dict` にフラグを設定
                    self.one_time_world_instance.ball.all_data_dict["newChannel_flag"] = True

                    # フラグファイルを削除し、ファイル名の保持を解除
                    os.remove(os.path.join(channel_dir, self.flag_file_name))
                    self.flag_file_name = None  # フラグファイル名をリセット
                    print(f"フラグファイル {file_name} を削除しました。")  # デバッグ用メッセージ

        return "Completed"
