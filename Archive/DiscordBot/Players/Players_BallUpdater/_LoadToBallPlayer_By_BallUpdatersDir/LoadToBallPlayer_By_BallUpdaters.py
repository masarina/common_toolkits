import os
import json
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
        
        # ball.all_data_dictにパスを追加
        self.one_time_world_instance.ball.all_data_dict["all_user_information_dict"] = one_time_world_instance.updateUIDPlayer.save_path
        
        """ all_user_information_dictの チャンネルID-UIDのペア情報 の更新 """
        # チャンネルと、チャンネル設立者の辞書のパスを取得
        created_channelID_and_userID_json_path = self.one_time_world_instance.channelCreatorCheckerPlayer.channel_creator_info_json_path
        

        return "Completed"
        
    def update_channelIDInfo(self,all_user_dict_json_path, channel_info_dict_json_path):
        # データを取得
        with open(all_user_dict_json_path, 'r') as json_file:
            all_user_dict = json.load(json_file)
        with open(channel_info_dict_json_path, 'r') as json_file:
            channel_info_dict = json.load(json_file)
            
        """ all_user_dictをアップデート """
        key_name = "having_channel"
        
        # まだ having_channel が未定義であれば、からのリストを作成
        for _, user_info_dict in all_user_dict.items()
            user_info_dict.setdefault(key_name, []) # keyが未定義の場合[]で初期化
        
        # all_user_dictを更新
        for ChID, UID in channel_info_dict:
            channel_list = all_user_dict[str(UID)][key_name]
            channel_list += ChID
            all_user_dict[str(UID)][key_name] = channel_list
        
        
        
        
        
        
        
        
