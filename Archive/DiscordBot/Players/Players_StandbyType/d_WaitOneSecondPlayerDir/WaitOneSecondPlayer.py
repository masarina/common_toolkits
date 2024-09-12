import asyncio
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class WaitOneSecondPlayer(SuperPlayer):
    def __init__(self):
        super().__init__()
        self.my_name = None

    def return_my_name(self):
        return "WaitOneSecondPlayer"

    async def main(self):
        """
        このメソッド実行直前に、self.one_time_world_instance に最新のworldインスタンスが代入されています。
        1秒間待機します。
        """
        print("1秒待機を開始します...")
        await asyncio.sleep(1)
        print("1秒待機が完了しました。")
        return "Completed"
