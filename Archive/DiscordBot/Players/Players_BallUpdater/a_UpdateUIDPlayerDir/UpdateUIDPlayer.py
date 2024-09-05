import os
import pickle
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class UpdateUIDPlayer(SuperPlayer):
    def __init__(self):
        super().__init__()  # スーパークラスの初期化メソッドを呼び出す
        self.my_name = None

    def return_my_name(self):
        return "UpdateUIDPlayer"

    def main(self):
        """
        SuperPlayerのメンバ変数。
        このmain実行する直前に
        SuperPlayerでself.one_time_world_instance に
        最新のworldを代入してあります。
        """

        # ピクルファイルのパスを設定
        save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_user_information_dict.pkl")
        
        # pickleファイルからデータを読み込む
        user_data_dict = self.load_data_from_pickle(save_path)

        # txtファイルから新しいIDを読み込む
        new_user_data = self.load_data_from_txt()

        # ピクルデータに存在しないIDを追加し、ランクも設定
        updated_data = self.update_pickle_data(user_data_dict, new_user_data)

        # データをpickleファイルに保存
        self.save_data_to_pickle(updated_data, save_path)

        # ボールにピクルのパスを追加
        self.one_time_world_instance.ball.all_data_dict["all_user_information_dict"] = save_path

        return "Completed"

    def load_data_from_pickle(self, file_path):
        """
        ピクルファイルからデータを読み込む関数。
        ファイルが存在しない場合は空の辞書を返す。
        """
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        else:
            return {}

    def load_data_from_txt(self):
        """
        保存しているtxtから全ユーザーのIDを取得し、辞書を作成する。
        """
        # txtファイルのパス
        txt_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_ids.txt")
        
        # 辞書データを初期化
        user_data_dict = {}
        
        if os.path.exists(txt_file_path):
            with open(txt_file_path, 'r') as file:
                user_ids = file.read().splitlines()
                
            for user_id in user_ids:
                # 新しいユーザーに id,user_rank の初期化を実装
                user_data_dict[user_id] = {"id": user_id, "user_rank": "visitor"}
        
        return user_data_dict

    def update_pickle_data(self, existing_data, new_data):
        """
        ピクルデータに新しいIDを追加する関数。
        既存のデータに存在しない新しいIDを追加し、user_rankも "visitor" に設定する。
        """
        for user_id, data in new_data.items():
            if user_id not in existing_data:
                # 新しいユーザーに id と user_rank を追加
                existing_data[user_id] = {
                    "id": user_id,
                    "user_rank": "visitor"
                }
        return existing_data


    def save_data_to_pickle(self, data, file_path):
        """
        データをpickleファイルに保存する関数。
        """
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
        print(f"データが {file_path} に保存されました。")

# メモ:
# このファイルは UpdateUIDPlayer クラスを含んでおり、
# - user_ids.txt からユーザーIDを取得し、ランクを "visitor" に設定して、
# - all_user_information_dict.pkl ファイルに存在しないIDを追加してpickleに保存します。
# BallPassSchedulePatternを利用して、他のプレイヤー間でこの情報を共有できます。

# 引用されたファイル:
# - user_ids.txt : ユーザーIDが保存されているテキストファイル。各IDは改行で区切られています。
# - all_user_information_dict.pkl : 全ユーザーID情報とランクが保存されるpickleファイル。このファイルは更新形式で使用されます。

# 作成されたファイル:
# - このファイル (UpdateUIDPlayer) : 上記の機能を実装したプレイヤーです。
