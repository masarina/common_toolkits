import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class SendDaijinMessagePlayer(SuperPlayer):
    def __init__(self):
        super().__init__()
        self.my_name = None

    def return_my_name(self):
        return "SendDaijinMessagePlayer"

    def main(self):
        """
        GPT-2を使って会話をするためのプレイヤー。
        """
        # モデルとトークナイザーをTransformersから取得
        model_name = "rinna/japanese-gpt2-medium"  # 日本語モデルを指定
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        model = GPT2LMHeadModel.from_pretrained(model_name)

        # 入力テキストを用意
        input_text = "こんにちは、調子はどう？"

        # テキストをトークン化
        inputs = tokenizer(input_text, return_tensors="pt")

        # モデルで推論
        with torch.no_grad():
            outputs = model.generate(inputs["input_ids"], max_length=100, num_return_sequences=1)

        # トークンをテキストに戻す
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        print(f"GPT-2の返答: {response}")
        return "Completed"
