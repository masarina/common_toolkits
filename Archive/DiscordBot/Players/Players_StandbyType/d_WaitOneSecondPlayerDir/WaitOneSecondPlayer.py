import asyncio
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class WaitOneSecondPlayer(SuperPlayer):
    def __init__(self):
        super().__init__()
        self.my_name = None

    def return_my_name(self):
        return "WaitOneSecondPlayer"

    def main(self):
        """
        このメソッド実行直前に、self.one_time_world_instance に最新のworldインスタンスが代入されています。
        メインの処理を実行します。
        
        → 非同期処理のrunメソッドを実行します。
        """
        print("1秒待機を開始します...")
        self.run()
        print("1秒待機が完了しました。")

    def run(self):
        asyncio.run(self.wait_one_second())

    async def wait_one_second(self):
        await asyncio.sleep(1)
