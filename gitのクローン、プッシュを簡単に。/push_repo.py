import os
import subprocess
import pickle

# 現在の作業ディレクトリを表示
current_dir = os.getcwd()
print(f"現在の作業ディレクトリ: {current_dir}")

# pickleからリポジトリ名とURLを読み取る
with open('repo_info.pkl', 'rb') as f:
    repo_info = pickle.load(f)
    repo_name = repo_info['repo_name']
    repo_url = repo_info['repo_url']

# クローンされたリポジトリのディレクトリに移動
repo_dir = os.path.join(current_dir, repo_name)
if os.path.exists(repo_dir):
    os.chdir(repo_dir)
    print(f"リポジトリディレクトリに移動: {repo_dir}")
else:
    print(f"エラー: リポジトリディレクトリが見つかりません: {repo_dir}")
    exit(1)

# SSHキーを追加（もし既に存在している場合はスキップされます）
ssh_key_path = os.path.expanduser("~/.ssh/id_rsa")
if not os.path.exists(ssh_key_path):
    subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-C", "your_email@example.com"])
    subprocess.run("eval $(ssh-agent -s)", shell=True)
    subprocess.run(["ssh-add", ssh_key_path])
    print("SSHキーを生成し、エージェントに追加しました。")
else:
    print("SSHキーは既に存在しています。")

# HTTPS URLをSSH URLに変換
ssh_url = repo_url.replace("https://github.com/", "git@github.com:")

# リモートURLをSSHに設定
subprocess.run(["git", "remote", "set-url", "origin", ssh_url])

# Gitのadd, commit, pushの実行
subprocess.run(["git", "add", "."])
commit_message = input("コミットメッセージを入力してください: ")
subprocess.run(["git", "commit", "-m", commit_message])
subprocess.run(["git", "push", "origin", "main"])

print(f"{repo_name} の内容がリポジトリにプッシュされました。")
