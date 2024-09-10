import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from ModelInference import ModelInference
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class SendDaijinMessagePlayer(SuperPlayer):
    def __init__(self):
        super().__init__()
        self.my_name = None

    def return_my_name(self):
        return "SendDaijinMessagePlayer"

    def main(self):
        """
        を使って会話をするためのプレイヤー。
        """       
        # 初期化
        all_data_dict = self.one_time_world_instance.ball.all_data_dict # 変数パスの簡易化
        progress_report_message = all_data_dict["progress_report_message"] # このKeyまだ未作成(2024-09-11)
        
        # モデルツールのインスタンス化(2回目以降はインスタンスを取得(処理軽量化の為))
        if all_data_dict["modelInference"] == None:
            all_data_dict["modelInference"] = ModelInference()
        modelInference = all_data_dict["modelInference"]
        
        # モデルの実行
        output_text = self.infer_with_rinna(progress_report_message, modelInference)
        
        
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
        listType_response = model_inference.infer_with_rinna(f"崩れた箇条書き:「\\n{listType_response}\\n」\\n\\n崩れた箇条書きを再度フォーマットしました:「\\n")

        # リストを見せて、推論させる。
        response_from_Daijin = model_inference.infer_with_rinna(f"今回の出来高:「\\n{listType_response}\\n」\\n\\n心理学系、行動経済学系、関数型プログラミング系のかわいい大臣ちゃんからの4ポイントアドバイス！:「\\n")
        
        return response_from_Daijin
        


