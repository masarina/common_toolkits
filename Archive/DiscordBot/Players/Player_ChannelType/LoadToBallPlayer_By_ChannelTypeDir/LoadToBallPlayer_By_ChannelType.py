import os
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class LoadToBallPlayer_By_ChannelType(SuperPlayer):
    def __init__(self):
        super().__init__()  # スーパークラスの初期化メソッドを呼び出す
        self.my_name = None

    def return_my_name(self):
        return "LoadToBallPlayer_By_ChannelType"

    def main(self):
        """
        JSONファイルのパスをball.all_data_dictに追加するプレイヤー。
        """
        
        # ball.all_data_dictにパスを追加
        self.one_time_world_instance.ball.all_data_dict["all_user_information_dict"] = one_time_world_instance.updateUIDPlayer.save_path
        
        # チャンネルと、チャンネル設立者の辞書のパスを取得（ボールの更新のプレイヤーの方で、この辞書もユーザーデータの情報として登録する時に、このパスを使っている）
        created_channelID_and_userID_json_path = self.one_time_world_instance.channelCreatorCheckerPlayer.channel_creator_info_json_path
        

        return "Completed"
        
        
