import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import ModelInference.ModelInference
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
        all_data_dict = self.one_time_world_instance.ball.all_data_dict
        
        # モデルツールの用意
        if all_data_dict["modelInference"] == None:
            all_data_dict["modelInference"] = ModelInference()
        modelInference = all_data_dict["modelInference"]
        
        

        return "Completed"
