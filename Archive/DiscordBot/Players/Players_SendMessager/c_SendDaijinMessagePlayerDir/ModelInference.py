import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, AutoModelForSequenceClassification, AutoTokenizer

class ModelInference:
    @staticmethod
    def infer_with_rinna(input_text):
        """
        rinnaモデルで推論するスタティックメソッド
        """
        model_name = "rinna/japanese-gpt2-medium"
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        model = GPT2LMHeadModel.from_pretrained(model_name)

        inputs = tokenizer(input_text, return_tensors="pt")

        with torch.no_grad():
            outputs = model.generate(inputs["input_ids"], max_length=100, num_return_sequences=1)

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    @staticmethod
    def infer_with_scibert(input_text):
        """
        論文を学習させたモデルで推論するスタティックメソッド
        """
        model_name = "allenai/scibert_scivocab_uncased"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)

        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True, max_length=512)

        with torch.no_grad():
            outputs = model(**inputs)
        
        # 出力から最大のスコアを持つラベルを取得
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
        return predicted_class

    @staticmethod
    def translate_japanese_to_english(text):
        model_name = "Helsinki-NLP/opus-mt-ja-en"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)

        inputs = tokenizer(text, return_tensors="pt", padding=True)
        translated = model.generate(**inputs)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
        return translated_text

    @staticmethod
    def translate_english_to_japanese(text):
        model_name = "Helsinki-NLP/opus-mt-en-ja"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)

        inputs = tokenizer(text, return_tensors="pt", padding=True)
        translated = model.generate(**inputs)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
        return translated_text
