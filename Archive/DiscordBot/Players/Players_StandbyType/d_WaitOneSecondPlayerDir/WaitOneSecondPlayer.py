import time
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class WaitOneSecondPlayer(SuperPlayer):
    def __init__(self):
        super().__init__()
        self.my_name = None

    def return_my_name(self):
        return "WaitOneSecondPlayer"

    def main(self):
        """
        このメソッド実行直前に、self.one_time_world_instance に
        最新のworldインスタンスが代入されています。
        """
        print(f"{self.return_my_name()} が実行されました。")
        self.run()
        return "Completed"

    def run(self):
        """
        1秒待機します。
        """
        print("1秒待機を開始します...")
        time.sleep(1)
        print("1秒待機が完了しました。")
