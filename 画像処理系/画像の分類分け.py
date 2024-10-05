"""
結構つかうので置いとく。雑だけど。torchもopencvもつかうから、予めインストールしておくこと。pandasの仮想環境をおすすめする。
"""

import os
import torch
import clip
from PIL import Image
import cv2
from datetime import datetime as dt
import shutil
current_dir = os.path.dirname(os.path.abspath(__file__))
import cv2.cuda as cv2cuda  # OpenCVのGPU版を利用

class FileMover:
    def __init__(self, source_dir, dest_dir, keywords):
        self.source_dir = source_dir
        self.dest_dir = dest_dir
        self.keywords = keywords
        # self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = "cpu" # 処理スピードそこまで変わらなかたので。
        self.model, self.preprocess = self.load_clip_model()

    def load_clip_model(self):
        model, preprocess = clip.load("ViT-B/32", device=self.device)
        return model, preprocess

    def is_image_file(self, filename):
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']
        return any(filename.lower().endswith(ext) for ext in image_extensions)

    def is_video_file(self, filename):
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.mpeg', '.mpg']
        return any(filename.lower().endswith(ext) for ext in video_extensions)

    def extract_video_frame(self, video_path):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None
        # 中央のフレームを取得
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count // 2)
        ret, frame = cap.read()
        cap.release()
        if ret:
            return frame
        else:
            return None


    def move_file(self, file_path):
        # 移動先ディレクトリにファイル名を追加して、移動先のパスを作成する
        dest_path = os.path.join(self.dest_dir, os.path.basename(file_path))
        
        # もし移動先に同じ名前のファイルがすでに存在していたら、ファイル名を変更して重複を避ける
        if os.path.exists(dest_path):
            # ファイル名と拡張子を分ける
            base, ext = os.path.splitext(os.path.basename(file_path))
            count = 1  # ファイル名の連番をつけるためのカウンター
            
            # 重複しないファイル名が見つかるまで繰り返す
            while True:
                # 新しいファイル名を作成する（例：ファイル名_1.jpg のように）
                new_filename = f"{base}_{count}{ext}"
                # 新しいファイル名で移動先のパスを作成する
                dest_path = os.path.join(self.dest_dir, new_filename)
                
                # その新しいファイル名が存在しない場合、ループを抜ける
                if not os.path.exists(dest_path):
                    break
                count += 1  # 存在する場合はカウントを増やして次のファイル名を試す
        
        # ファイルを移動先のディレクトリに移動する
        shutil.move(file_path, dest_path)
        # 移動が完了したことを表示する
        print(f"Moved: {file_path} -> {dest_path}")


    def match_image_with_keywords(self, image):
        image_input = self.preprocess(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))).unsqueeze(0).to(self.device)
        text_inputs = clip.tokenize(self.keywords).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
            text_features = self.model.encode_text(text_inputs)

        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarity = (image_features @ text_features.T).squeeze(0)

        threshold = 0.3  # 必要に応じて調整。(どれだけ言葉と合致しているか。0.3がちょうどよかった。2024-10-06)
        return similarity.max().item() > threshold

    def process_image(self, file_path, image):
        if self.match_image_with_keywords(image):
            self.move_file(file_path)
            
            

    def process_files(self):
        # ファイル数のカウント
        total_files = sum([len(files) for _, _, files in os.walk(self.source_dir)])
        processed_files = 0

        # ソースディレクトリ内のファイルを再帰的に処理
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # 画像ファイルの処理
                if self.is_image_file(file):
                    image = cv2.imread(file_path)
                    if image is not None:
                        self.process_image(file_path, image)
                # 動画ファイルの処理
                elif self.is_video_file(file):
                    frame = self.extract_video_frame(file_path)
                    if frame is not None:
                        self.process_image(file_path, frame)
                
                # 進捗バーの更新
                processed_files += 1
                self.print_progress_bar(processed_files, total_files)


    def print_progress_bar(self, processed, total, length=50):
        percent = (processed / total) * 100
        filled_length = int(length * processed // total)
        bar = '█' * filled_length + '-' * (length - filled_length)
        print(f'\rProgress: |{bar}| {percent:.2f}% Complete', end='\r')

    def run(self):
        print("Starting file processing...")
        self.process_files()
        print("\nFile processing complete!")


def create_directory_with_system(dir_path):
    command = f'sudo -H mkdir -p "{dir_path}"'
    result = os.system(command)  # コマンドの実行結果を取得
    if result == 0:
        print(f"Directory created successfully: {dir_path}")
    else:
        print(f"Failed to create directory: {dir_path}, status code: {result}")


def search_dir_setting(search_dir=None,nowtime_ver=None):
    """
    検索する場所のリストを返します。
    ややこしいですが、以前分類した分類先のディレクトリも、検索範囲とするための処理も含みます。
    そのため、ココでは分類分け後のディレクトリも自動で作成します。
    自動で作成することで、次回、今回分類した先のディレクトリも検索範囲に含めやすくできるからです。
    
    """
    
    """ 初期化 """
    search_dir # 検索するディレクトリパス
    search_dir_paths = [] # 以前に分類分けしたディレクトリ（これも検索する範囲に入れる処理が、このメソッド。）
    
    """ 以前に分類分けしたディレクトリパスを作成します。 """
    ver = 0
    while True:
        
        try:
            # キーワードの一番最後の要素を、保存先ディレクトリ名(ここでは検索先ディレクトリ)とします。
            keywords = select_version(ver=ver) # バージョンを一つ指定し、そのバージョンのキーワードを取得
            dir_path = f"{current_dir}/{keywords[-1]}" # ディレクトリパスを作成
            
            # ディレクトリが存在しない場合は作成
            create_directory_with_system(dir_path)

            # もし今回のバージョンであれば、検索範囲に入れない。（保存先も検索範囲に入れてしまっても意味ないので、、。）
            if nowtime_ver == ver:
                pass

            else:
                # 検索範囲を追加。
                search_dir_paths.append(dir_path)
            
            # 次のバージョンへ移行。
            ver += 1

        except UnboundLocalError:
            break # 全てのバージョンのディレクトリパスが作成できたら、ループを出る。

        except Exception as e:
            # 他のエラーが発生した場合に、そのエラーメッセージを表示
            print(f"An error occurred: {str(e)}")
            break
        
    search_dir_paths.append(search_dir) # 今回の検索パスも追加して、返す。
    return search_dir_paths



"""
自由に設定する項目 ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
"""
def select_version(ver=None):
    """
    好きなように追加してください。
    """
    if ver == 0:
        keywords = ["笑顔","笑っている", "にっこり"] # or検索。

    elif ver == 1:
        keywords = ["足", "裸足", "足の根本", "ふともも"] # or検索。

    elif ver == 2:
        keywords = ["魚"] # or検索。

    # テンプレート
    elif ver == 3:
        keywords = ["ワード1","ワード2"] # or検索。
        
    return keywords

if __name__ == "__main__":
    """
    select_version内に設定した、バージョンごとにディレクトリが作成され、そのディレクトリ内にワードに一致したものが保存されます。
    分類先はこのファイルが存在しているディレクトリ層に保存されます。
    """
  
    """ 初期化 """
    for i in range(4):
    
        # 設定
        ver = i
        search_dir = "/"  # 検索元ディレクトリpath

        # キーワードを取得。
        keywords= select_version(ver=ver)
        
        # 分類分け先のディレクトリ
        save_dir_path = keywords[-1]
        
        # 検索先の選択(選択したディレクトリの内部ディレクトリ先まで、自動で検索されます。)
        search_dir_paths = search_dir_setting(search_dir=search_dir, nowtime_ver=ver) 
        
        # 全ての検索ディレクトリを、検索
        for search_path_point in search_dir_paths:
            print(f"\n\033[34m====\n【検索場所】\n{search_path_point} \n\n【サーチワード】\n{keywords}\n\n【保存先】\n{save_dir_path}\n====\033[0m")
            mover = FileMover(
                search_path_point, # 検索する場所のディレクトリ
                save_dir_path,  # ファイルを移動する先のディレクトリ名
                keywords, # キーワード
            )
            mover.run()
