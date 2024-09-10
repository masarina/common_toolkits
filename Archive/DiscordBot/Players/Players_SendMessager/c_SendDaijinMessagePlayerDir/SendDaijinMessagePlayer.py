import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class RinnaGPT2DecodePlayer(SuperPlayer):
    def __init__(self):
        super().__init__()
        self.my_name = None

    def return_my_name(self):
        return "RinnaGPT2DecodePlayer"

    def main(self):
        """
        を使って会話をするためのプレイヤー。
        """       

        return "Completed"
