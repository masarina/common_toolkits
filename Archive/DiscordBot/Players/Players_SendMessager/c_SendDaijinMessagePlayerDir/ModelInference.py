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
            outputs = model.generate(inputs["input_ids"], max_length=1024, num_return_sequences=1)

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

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
