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
        elif self.schedule_mode == 'Mode_Standby':
            
            # 新しいメンバー加入時の処理
            if world.ball.all_data_dict["newUser_flag"]:
                self.schedule_mode = 'Mode_NewUserThenTask'
            
            # 新しいメッセージがポストされた時の処理
            elif world.ball.all_data_dict["newMessage_flag"]:
                self.schedule_mode = 'Mode_NewMessageThenTask'
            
            # 新しいチャンネルが作成された時の処理
            elif world.ball.all_data_dict["newChannel_flag"]:
                self.schedule_mode = 'Mode_NewChannelThenTask'
            
            # 何もフラグがなければ、スタンバイモードを保持
            else:
                self.schedule_mode = 'Mode_Standby'

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
                [['DebugPlayer'],['InitDiscordBotPlayer']], # Discordボットをインスタンス化
                [['FinalPlayer']]  # 例: 第二ミニスケジュール
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
            
            
        elif mode_name == "Mode_NewUserThenTask":
            array_2d = [
                [['FirstPlayer']],  # 例: 第一ミニスケジュール
                [['LoadToBallPlayer_By_ChannelType']], # 新メンバーにチャンネルを作成してあげるため。
                [['UpdateUIDPlayer']],
                [['LoadToBallPlayer_By_MessageType']],
                [['WelcomeNewUserPlayer']], # ウェルカムメッセージ
                [['CreateChannelPlayer']], # 新メンバーにチャンネルを作ってあげる
                [['RankUpPlayer']], # visitorからnewUserにランクアップさせる
                [['FinalPlayer']]  # 例: 第二ミニスケジュール
            ]
            
        elif mode_name == "Mode_NewMessageThenTask":
            array2d = [
                [['FirstPlayer']],
                [['LoadToBallPlayer_By_MessageType']],
                [['DaijinMessageMakePlayer']],
                [['SendMessagePlayer']],
                [['FinalPlayer']]
            ]
            
        elif mode_name == "Mode_NewChannelThenTask":
            array2d = [
                [['FirstPlayer']],
                [['LoadToBallPlayer_By_ChannelType']], # ChannelType全般の初期化
                [['ChannelCreatorCheckerPlayer']], # UIDとChIDの辞書を作る
                [['LoadToBallPlayer_By_MessageType']], # MessageType全般の初期化
                [['SendToChannelMakingUserPlayer']] # このチャンネル作成者にメッセージ。
                [['FinalPlayer']]
            ]

        elif mode_name == "end":
            print("プログラムが完了しました。確認してください。")
            exit(0)


        if array_2d == None:
            print("モードの選択が出来ませんでした。モード名を確認してください。")
            exit(1)
        
        self.now_schedule = array_2d        







