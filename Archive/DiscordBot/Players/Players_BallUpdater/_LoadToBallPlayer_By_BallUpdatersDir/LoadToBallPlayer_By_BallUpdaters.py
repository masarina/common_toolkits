import os
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class LoadToBallPlayer_By_BallUpdaters(SuperPlayer):
    def __init__(self):
        super().__init__()  # スーパークラスの初期化メソッドを呼び出す
        self.my_name = None

    def return_my_name(self):
        return "LoadToBallPlayer_By_BallUpdaters"

    def main(self):
        """
        JSONファイルのパスをball.all_data_dictに追加するプレイヤー。
        """

        # JSONファイルのパスを構築
        json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_user_information_dict.json")
        
        # ball.all_data_dictにパスを追加
        self.one_time_world_instance.ball.all_data_dict["all_user_information_dict"] = json_file_path

        return "Completed"
