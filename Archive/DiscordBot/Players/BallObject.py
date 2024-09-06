import copy
import sys 
sys.path.append('/etc/api_store')

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
        
        
        """
        デバッグ用（メンバ変数は全てDebugPlayerがデバッグしてくれます。）
        """
        self.now_catch_balling_player = None
        self.next_player_name = None

    def schedule_mode_settings(self, world=None):
        
        # トレーニングデータをダウンロード
        if self.schedule_mode == 'Mode_First':
            self.schedule_mode = 'Mode_Standby'

        # データをフォーマット
        elif self.schedule_mode == 'Mode_DataDownload':
            self.schedule_mode = 'Mode_TrainingDataFormat'
            

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
            
        elif mode_name == "Mode_Standby":
            array_2d = [
                [['FirstPlayer']],  # 例: 第一ミニスケジュール
                [['OneSecondWeightPlayer']],
                [['DiscordMemberTrackerPlayer']],
                [['DiscordMessageTrackerPlayer']],
                [['DiscordChannelTrackerPlayer']],
                [['FinalPlayer']]  # 例: 第二ミニスケジュール
            ]
            

        elif mode_name == "end":
            print("プログラムが完了しました。確認してください。")
            exit(0)


        if array_2d == None:
            print("モードの選択が出来ませんでした。モード名を確認してください。")
            exit(1)
        
        self.now_schedule = array_2d        







