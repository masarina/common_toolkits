import torch
import json
import subprocess
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from ModelInference import ModelInference
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class SendDaijinMessagePlayer(SuperPlayer):
    def __init__(self):
        super().__init__()
        self.my_name = None
        
        # MessageKeeper.pyを並行実行
        messageKeeper_path = f"{os.path.dirname(os.path.abspath(__file__))}/MessageKeeper.py"
        subprocess.Popen(['python',messageKeeper_path])

    def return_my_name(self):
        return "SendDaijinMessagePlayer"

    def main(self):
        """
        を使って会話をするためのプレイヤー。
        """       
        # 初期化
        ## 変数パスの簡易化
        all_data_dict = self.one_time_world_instance.ball.all_data_dict 
        
        # このファイルが保存されているディレクトリパスを取得
        thisDir_path = os.path.dirname(os.path.abspath(__file__))
        
        # JSONファイルのパスを設定
        json_path = os.path.join(thisDir_path, 'messages.json')
        
        # JSONファイルを開いて辞書として読み込む
        with open(json_path, 'r') as json_file:
            UID_MESSE_dict = json.load(json_file)

        # 辞書からユーザIDとメッセージのペアを一つ取得
        # .items()で辞書のキーと値のペアを取得する
        if UID_MESSE_dict:
            report_user_id, progress_report_message = UID_MESSE_dict.popitem()
        else:
            print("辞書が空です。")
        
        # モデルツールのインスタンス化(2回目以降はインスタンスを取得(処理軽量化の為))
        if all_data_dict["modelInference"] == None:
            all_data_dict["modelInference"] = ModelInference()
        modelInference = all_data_dict["modelInference"]
        
        # モデルの実行
        output_text = self.infer_with_rinna(progress_report_message, modelInference)
        
        # 大臣からのメッセージをballに保存
        self.one_time_world_instance.ball.all_data_dict["DaijinMessage_of_progressReport"] = output_text
        
        
        return "Completed"
        
    def infer_with_rinna(self, input_text, model_inference):
        """
        rinnaモデルで推論するメソッド
        入力テキストが500文字を超えた場合、500文字ごとに区切って処理する。
        """
        # 500文字ごとにテキストを分割
        chunk_size = 500
        input_chunks = [input_text[i:i + chunk_size] for i in range(0, len(input_text), chunk_size)]
    
        responses = []
    
        # 各チャンクに対して推論を実行
        for chunk in input_chunks:
            input_text = f"文章:｢\\n{chunk}\\n｣\\n\\nこの文章をできる限り内容を詳細に保つ形で、かつ箇条書きにまとめました:\\n「"
            rinna_response = model_inference.infer_with_rinna(input_text)
            formated_response = rinna_response[:-2]
            responses.append(formated_response)
    
        # 全てのチャンクの結果を統合
        listType_response = "".join(responses)
        
        # 整頓する
        listType_response = (model_inference.infer_with_rinna(f"崩れた箇条書き:「\\n{listType_response}\\n」\\n\\n崩れた箇条書きを再度フォーマットしました:「\\n"))[:-2]
        
        # 内容の題名を作る
        report_name = f"# {(model_inference.infer_with_rinna(f"実行した事柄:「\\n{listType_response}\\n」\\n\\nそうですね、あなたが今日頑張って実行したこのタスクリストに題名を付けるとするならば、次のようになるでしょう！:「\\n"))[:-2]}"

        # リストを見せて、推論させる。
        response_from_Daijin = (model_inference.infer_with_rinna(f"今回の出来高:「\\n{listType_response}\\n」\\n\\n心理学系、行動経済学系、関数型プログラミング系のかわいい大臣ちゃんからの4ポイントアドバイス！:「\\n"))[:-2]}"
        
        return response_from_Daijin
        


