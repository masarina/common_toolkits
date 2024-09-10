import os
import json
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class UpdateUIDPlayer(SuperPlayer):
    def __init__(self):
        super().__init__()  # スーパークラスの初期化メソッドを呼び出す
        self.my_name = None
        self.save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_user_information_dict.json")

    def return_my_name(self):
        return "UpdateUIDPlayer"

    def main(self):
        """
        SuperPlayerのメンバ変数。
        このmain実行する直前に
        SuperPlayerでself.one_time_world_instance に
        最新のworldを代入してあります。
        """

        # JSONファイルのパスを設定
        save_path = self.save_path
        
        # JSONファイルからデータを読み込む
        user_data_dict = self.load_data_from_json(save_path)

        # txtファイルから新しいIDを読み込む
        new_user_data = self.load_data_from_txt()

        # JSONデータに存在しないIDを追加し、ランクも設定
        updated_data = self.update_json_data(user_data_dict, new_user_data)

        # データをJSONファイルに保存
        self.save_data_to_json(updated_data, save_path)

        # ボールにJSONのパスを追加
        self.one_time_world_instance.ball.all_data_dict["all_user_information_dict"] = save_path

        return "Completed"

    def load_data_from_json(self, file_path):
        """
        JSONファイルからデータを読み込む関数。
        ファイルが存在しない場合は空の辞書を返す。
        """
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
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

    def update_json_data(self, existing_data, new_data):
        """
        JSONデータに新しいIDを追加する関数。
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
        
    def create_channel_of_visitorUser(self):
        self.one_time_world_instance.ball.all_data_dict["category_id"] =   # カテゴリIDを取得
        self.one_time_world_instance.ball.all_data_dict["channel_name"]  # チャンネル名を取得
        self.one_time_world_instance.ball.all_data_dict["bot_instance"]  # botインスタンスを取得
        

    def save_data_to_json(self, data, file_path):
        """
        データをJSONファイルに保存する関数。
        """
        with open(file_path, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"データが {file_path} に保存されました。")
