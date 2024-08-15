import os
import subprocess
import pickle

# メールアドレスやIDを設定
git_user = "youer_Name"
git_email = "youre_email.com"

# Gitの設定を反映
subprocess.run(["git", "config", "--global", "user.name", git_user])
subprocess.run(["git", "config", "--global", "user.email", git_email])

# リポジトリのURLを入力
repo_url = input("リポジトリのURLを入力してください: ")

# クローン先のディレクトリ名を決定（リポジトリ名を利用）
repo_name = os.path.basename(repo_url).replace(".git", "")
if not os.path.exists(repo_name):
    os.mkdir(repo_name)

# リポジトリ名をpickleで保存
with open('repo_info.pkl', 'wb') as f:
    pickle.dump({'repo_name': repo_name}, f)

# クローンを実行
subprocess.run(["git", "clone", repo_url, repo_name])

print(f"リポジトリが {repo_name} にクローンされました。")
