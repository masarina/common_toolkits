import copy
import sys 
sys.path.append('/etc/api_store')
from ALPHAVANTAGE_API import ALPHAVANTAGE_API 
from ALPACA_API import ALPACA_API

class BallObject:
    """
    このクラスはWorldクラスでインスタンス化されます。
    """
    def __init__(self):
        """
        デザインパターン用
        """
        # 変数の用意
        self.now_schedule = None
        self.now_schedule_status = None
        self.schedule_mode = None  # 初期スケジュールモード
        self.index_of_schedule = 0 # 本スケジュール
        self.index_of_schedule_of_schedule = 0 # スケジュール内のスケジュール
        self.schedule_mode = "Mode_First" # 一番最初のモードを選択。
        self.schedule_dict(mode_name=self.schedule_mode) # スケジュールをセット。
        self.reset_schedule_status() # ステータスの初期化。
        
        """
        今回の本プログラミング用
        """
        # 全ての情報を格納する辞書の用意
        self.all_data_dict = {}
        
        # インスタンスの用意
        aLPHAVANTAGE_API = ALPHAVANTAGE_API()
        aLPACA_API = ALPACA_API()
        
        # apiの取得
        aLPHAVANTAGE_API_OPEN_KEY = aLPHAVANTAGE_API.API_OPEN_KEY # アルファバンテージ
        aLPHAVANTAGE_API_QUERY_URL = aLPHAVANTAGE_API.QUERY_URL # アルファバンテージ
        aLPACA_API_OPEN_KEY = aLPACA_API.API_OPEN_KEY # アルパカ
        aLPACA_API_SECRET_KEY = aLPACA_API.API_SECRET_KEY # アルパカ
        aLPACA_API_BASE_URL = aLPACA_API.BASE_URL # アルパカ
        self.all_data_dict.update(
            {
            "aLPHAVANTAGE_API_OPEN_KEY":aLPHAVANTAGE_API_OPEN_KEY,
            "aLPHAVANTAGE_API_QUERY_URL":aLPHAVANTAGE_API_QUERY_URL,
            "aLPACA_API_OPEN_KEY":aLPACA_API_OPEN_KEY,
            "aLPACA_API_SECRET_KEY":aLPACA_API_SECRET_KEY,
            "aLPACA_API_BASE_URL":aLPACA_API_BASE_URL
            }
        ) 
        
        
        """
        デバッグ用（メンバ変数は全てDebugPlayerがデバッグしてくれます。）
        """
        self.now_catch_balling_player = None
        self.next_player_name = None

    def schedule_mode_settings(self, world=None):
        
        # トレーニングデータをダウンロード
        if self.schedule_mode == 'Mode_First':
            self.schedule_mode = 'Mode_DataDownload'

        # データをフォーマット
        elif self.schedule_mode == 'Mode_DataDownload':
            self.schedule_mode = 'Mode_TrainingDataFormat'
            
        # 学習開始
        elif self.schedule_mode == 'Mode_TrainingDataFormat':
            self.schedule_mode = "Mode_Training"

        # 推論結果を保持する変数の用意
        elif self.schedule_mode == 'Mode_Training':
            self.schedule_mode = "Mode_ResetPredictedLog"

        # 推論用データを「ダウンロード、フォーマット、推論」までを実施。
        elif self.schedule_mode == 'Mode_ResetPredictedLog':
            self.schedule_mode = "Mode_DataFormat_And_Prediction_AllCompany"
            
        # 全ての銘柄の「ダウンロード、フォーマット、推論」が完了していない場合、このモードを繰り返す。
        elif self.schedule_mode == 'Mode_DataFormat_And_Prediction_AllCompany' and world.ball.all_data_dict["all_predictions_complete"] != True:
            self.schedule_mode = "Mode_DataFormat_And_Prediction_AllCompany"

        # 全ての銘柄の推論が完了した場合、トレード結果を保持する変数の用意
        elif self.schedule_mode == 'Mode_DataFormat_And_Prediction_AllCompany' and world.ball.all_data_dict["all_predictions_complete"] == True:
            self.schedule_mode = "Mode_ResetTradedLog"

        # トレード開始
        elif self.schedule_mode == 'Mode_ResetTradedLog':
            self.schedule_mode = "Mode_Trading_AllCompany"

        # 全ての銘柄のトレードが完了していない場合、このモードを繰り返す。
        elif self.schedule_mode == 'Mode_Trading_AllCompany' and world.ball.all_data_dict['all_Trade_complete'] != True:
            self.schedule_mode = 'Mode_Trading_AllCompany'
        
        # 全ての銘柄のトレードが完了した場合、UTC時間23:59まで待機する。
        elif self.schedule_mode == 'Mode_Trading_AllCompany' and world.ball.all_data_dict['all_Trade_complete'] == True:
            self.schedule_mode = 'Mode_WeightAndStart_UTC2359'

        # 待機が完了した場合、再度「推論 〜 トレード」までを実施する
        elif self.schedule_mode == 'Mode_WeightAndStart_UTC2359':
            self.schedule_mode = "Mode_ResetPredictedLog"
            
        else:
            print(f"{self.schedule_mode} というスケジュールモードは存在しません。BallObjectの「schedule_mode_settings」と「schedule_dict」を確認してください。")
            exit(1)


        # ifで選択されたモードのスケジュールを、メンバ変数に反映させる。
        self.schedule_dict(mode_name=self.schedule_mode)


    def reset_schedule_status(self):
        keep = copy.deepcopy(self.now_schedule)

        self.now_schedule_status = self.now_schedule
        for mini_schedule in range(len(self.now_schedule_status)):
            for players_status in range(len(self.now_schedule_status[mini_schedule])):
                self.now_schedule_status[mini_schedule][players_status] = "None"

        self.now_schedule = keep


    def schedule_dict(self,mode_name=None):
        array_2d = None
        
        if mode_name == "Mode_First":
            array_2d = [
                [['FirstPlayer']],  # 例: 第一ミニスケジュール
                [['DebugPlayer'],['FinalPlayer']]  # 例: 第二ミニスケジュール
            ]
            
        elif mode_name == "Mode_DataDownload":
            array_2d = [
                [['FirstPlayer']],  # 例: 第一ミニスケジュール
                [['DownloadTrainingDataPlayer']],
                [['FinalPlayer']]  # 例: 第二ミニスケジュール
            ]

        elif mode_name == "Mode_TrainingDataFormat":
            array_2d = [
                [['FirstPlayer']],  # 例: 第一ミニスケジュール
                [['NormalizeByPreviousDayAs100PercentPlayer']],
                [['AppendWinLosePlayer']],
                [['AppendNextDayInfoPlayer']],
                [['NormalizeClosePctPlayer']],
                [['DropColumnsPlayer']],
                [['TimeSeriesFormatterPlayer']],
                [['OverlapDataPlayer']],
                [['TransformDataPlayer']],
                [['RemoveNoneRowsPlayer']],
                [['AddPrefixPlayer']],
                [['AddSpecialTokensPlayer']],
                [['SplitDataPlayer']],
                [['ConvertCsvToTxtPlayer']],
                [['SaveBallToPicklePlayer']],
                [['FinalPlayer']]
            ]


        elif mode_name == "Mode_Training":
            array_2d = [
                [['FirstPlayer']],  # 例: 第一ミニスケジュール
                [['LoadPickleToBallPlayer']],
                [['SetupGpt2Player']],
                [['SetupTokenizerPlayer']],
                [['TrainingPlayer'],['SaveTrainedBallToPicklePlayer']],
                [['FinalPlayer']]  # 例: 第nミニスケジュール
            ]

        elif mode_name == "Mode_ResetPredictedLog":
            array_2d = [
                [['FirstPlayer']],  # 例: 第一ミニスケジュール
                [['ResetPredictedLogPlayer']],  # 全ての銘柄の推論結果がdict型で格納される。それを全てNoneにするプレイヤー。
                [['CheckAllPredictionsCompletePlayer']], # 全ての銘柄の推論完了でTrueにするflagの、リセット。
                [['FinalPlayer']]  # 例: 第二ミニスケジュール
            ]

        elif mode_name == "Mode_DataFormat_And_Prediction_AllCompany":
            array_2d = [
                [['FirstPlayer']],  # 例: 第一ミニスケジュール
                
                [['SelectNextCurrencyPlayer']],  # 推論する銘柄を1つ選択し、ballに保存。
                [['DownloadTwoMonthsDataPlayer']], # 銘柄のデータをダウンロード
                [['ExecuteNormalizationPlayer']], # 銘柄1つ分のデータのフォーマット開始
                [['ExecuteAppendWinLosePlayer']],
                [['ExecuteAppendNextDayInfoPlayer']],
                [['ExecuteNormalizeClosePctPlayer']],
                [['ExecuteDropColumnsPlayer']],
                [['ExecuteTimeSeriesFormatterPlayer']],
                [['ExecuteOverlapDataPlayer']],
                [['ExecuteTransformDataPlayer']],
                [['ExecuteAddPrefixPlayer']],
                [['AddTopSpecialTokenPlayer']],
                [['CsvToSpaceSeparatedTxtPlayer']],
                [['RemoveRightmostColumnTxtPlayer']], # 銘柄1つ分のデータのフォーマット完了
                
                [['InferencePlayer']], # この銘柄を推論
            
                [['UpdatePredictedLogPlayer']], # 銘柄1つ、推論が完了したので、結果をballに記録する。
                [['CheckAllPredictionsCompletePlayer']], #全ての銘柄の推論が完了していれば、all_predictions_complete に True を代入します。
                
                [['FinalPlayer']]
            ]
            
            

        elif mode_name == "Mode_ResetTradedLog":
            array_2d = [
                [['FirstPlayer']],  # 例: 第一ミニスケジュール
                [['ResetTradedLogPlayer']], # トレード結果を記録する辞書のリセット
                [['TradeFlagMakePlayer']], # 全ての銘柄のトレードが完了した時、all_Trade_complete を True とするが、そのall_Trade_completeの変数をballに用意するプレイヤー。
                [['FinalPlayer']]
            ]
            
        elif mode_name == "Mode_Trading_AllCompany":
            array_2d = [
                [['FirstPlayer']],  # 例: 第一ミニスケジュール
                [['SelectNextTradeCurrencyPlayer']], # トレードする銘柄名を、1つ抽出。
                [['TradeExecutionPlayer']], # この銘柄を、推論結果を元に、トレードする。
                [['CheckAllTradesCompletePlayer']], # 全ての銘柄のトレードが完了したとき、all_Trade_complete に True を代入するプレイヤー。
                [['FinalPlayer']]
            ]
            
            
        elif mode_name == "Mode_WeightAndStart_UTC2359":
            array_2d = [
                [['FirstPlayer']],  # 例: 第一ミニスケジュール
                [['WaitForTimeZonePlayer']], # 無限whileループに入る。UTC時間23:59になった時、whileを抜け出すプレイヤー。
                [['FinalPlayer']]
            ]
            
            

        elif mode_name == "end":
            print("プログラムが完了しました。確認してください。")
            exit(0)


        if array_2d == None:
            print("モードの選択が出来ませんでした。モード名を確認してください。")
            exit(1)
        
        self.now_schedule = array_2d        







