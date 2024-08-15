import os
import subprocess
import pickle

# pickleからリポジトリ名を読み取る
with open('repo_info.pkl', 'rb') as f:
    repo_info = pickle.load(f)
    repo_name = repo_info['repo_name']

# プッシュするディレクトリに移動
os.chdir(repo_name)

# Gitのadd, commit, pushの実行
subprocess.run(["git", "add", "."])
commit_message = input("コミットメッセージを入力してください: ")
subprocess.run(["git", "commit", "-m", commit_message])
subprocess.run(["git", "push"])

print(f"{repo_name} の内容がリポジトリにプッシュされました。")
