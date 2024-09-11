import torch
import json
import subprocess
import asyncio
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from ModelInference import ModelInference
from Players_CommonPlayers.SuperPlayerDir.SuperPlayer import SuperPlayer

class DaijinMessageMakePlayer(SuperPlayer):
    def __init__(self):
        super().__init__()
        self.my_name = None
        
        # MessageKeeper.pyを並行実行
        messageKeeper_path = f"{os.path.dirname(os.path.abspath(__file__))}/MessageKeeper.py"
        subprocess.Popen(['python',messageKeeper_path])

    def return_my_name(self):
        return "DaijinMessageMakePlayer"

    def main(self):
        """
        を使って会話をするためのプレイヤー。
        """       
        # 初期化
        ## 変数パスの簡易化
        all_data_dict = self.one_time_world_instance.ball.all_data_dict 
        bot_instance = all_data_dict["bot_instance"] # botインタンスを取得
        
        # このファイルが保存されているディレクトリパスを取得
        thisDir_path = os.path.dirname(os.path.abspath(__file__))
        
        # JSONファイルのパスを設定
        json_path = os.path.join(thisDir_path, 'messages.json')
        
        # JSONファイルを開いて辞書として読み込む
        with open(json_path, 'r') as json_file:
            messages_dict = json.load(json_file)

        # 辞書からデータを一つ取得
        if messages_dict:
            # 日付時刻をキーにして、ユーザーID、チャンネルID、メッセージ内容を取得
            timestamp, message_data = messages_dict.popitem()
            report_user_id = message_data['user_id']
            reported_channels_id = message_data['channel_id']
            progress_report_message = message_data['message']
        else:
            print("メッセージ辞書が空です。")
            return "No messages"
        
        # モデルツールのインスタンス化(2回目以降はインスタンスを取得(処理軽量化の為))
        if all_data_dict["modelInference"] == None:
            all_data_dict["modelInference"] = ModelInference()
        modelInference = all_data_dict["modelInference"]
        
        # モデルの実行、テキストの作成
        output_text, report_name = self.infer_with_rinna(progress_report_message, modelInference, report_user_id)
        
        # サブテキストの作成
        reported_channels_name = self.get_channel_name_by_id(all_data_dict["bot_instance"], reported_channels_id)
        reported_user_name = self.get_user_name_by_if(all_data_dict["bot_instance"], report_user_id)
        sub_text = f"============================\n# {reported_channels_name}\n【報告者：{reported_user_name} より】\n\n[報告内容]\n# ```{report_name}```\n```{progress_report_message}```\n============================"
        
        # 大臣からのメッセージ、メッセージの送信先チャンネルIDをballに保存
        self.one_time_world_instance.ball.all_data_dict["send_message_player_message"] = output_text
        self.one_time_world_instance.ball.all_data_dict["send_message_player_channel_id"] = all_data_dict["channelID_【私達の進捗報告】"]
        
        
        return "Completed"
        
    def infer_with_rinna(self, input_text, model_inference, report_user_id):
        """
        rinnaモデルで推論するメソッド
        入力テキストが500文字を超えた場合、500文字ごとに区切って処理する。
        """
        # メッセージ送信者の名前を取得
        reporter_name = self.get_user_name_by_id(report_user_id)
        
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
        report_name = f"# {(model_inference.infer_with_rinna(f"実行した事柄:「\\n{listType_response}\\n」\\n\\nそうですね、{reporter_name}さんが今日頑張って実行したこのタスクリストに題名を付けるとするならば、次のようになるでしょう！:「\\n"))[:-2]}"

        # リストを見せて、推論させる。
        response_from_Daijin = (model_inference.infer_with_rinna(f"ペンネーム {reporter_name} さん の出来高:「\\n{listType_response}\\n」\\n\\n心理学系、行動経済学系、関数型プログラミング系で、かわいい大臣ちゃんからの4ポイントアドバイス！:「\\n"))[:-2]
        
        return response_from_Daijin, report_name
        
    def get_user_name_by_id(self, bot, user_id):
        """
        DiscordのBotインスタンスとユーザーIDを引数にとり、
        ユーザーIDを元に、そのユーザーの名前を取得して返す。
        """
        async def fetch_user_name():
            user = await bot.fetch_user(user_id)
            return user.name
    
        # 非同期関数を同期的に実行して、ユーザー名を取得
        return asyncio.run(fetch_user_name())



    def get_channel_name_by_id(self, bot_instance, channel_id):
        """
        チャンネルIDをもとに、チャンネル名を同期的に取得するメソッド。
        引数：
        - bot_instance: DiscordのBotインスタンス
        - channel_id: 取得したいチャンネルのID
        """
    
        async def fetch_channel_name():
            # チャンネルIDからチャンネルオブジェクトを取得
            channel = bot_instance.get_channel(channel_id)
            if channel:
                return channel.name
            else:
                raise ValueError(f"チャンネルID {channel_id} に該当するチャンネルが見つかりません。")
    
        # 非同期関数を同期的に実行して、チャンネル名を取得
        return asyncio.run(fetch_channel_name())


