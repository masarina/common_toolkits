import os
import ModelInference
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class LoadToBallPlayer_By_MessageType(SuperPlayer):
    def __init__(self):
        super().__init__()  # スーパークラスの初期化メソッドを呼び出す
        self.my_name = None

    def return_my_name(self):
        return "LoadToBallPlayer_By_MessageType"

    def main(self):
        """
        MessageTypeメソッド群のイニシャライザ的存在
        """
        
        # ball.all_data_dictにパスを追加
        self.one_time_world_instance.ball.all_data_dict["all_user_information_dict"] = one_time_world_instance.updateUIDPlayer.save_path
        
        # カテゴリー【プロジェクト】のカテゴリID
        self.one_time_world_instance.ball.all_data_dict["categoryID_of_ProjectCategory"] = 1195503636453793792
        
        # 推論モデルのインスタンス化を登録
        modelInference = ModelInference.ModelInference()
        self.one_time_world_instance.ball.all_data_dict["modelInference"] = modelInference
        

        return "Completed"
