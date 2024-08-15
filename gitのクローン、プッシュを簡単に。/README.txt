SSHキーを発行して、gitに登録する必要があります。


rm -rf ~/.ssh/id_rsa ~/.ssh/id_rsa.pub
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

cat ~/.ssh/id_rsa.pub # これをコピーしてhttps://github.com/settings/keysで設定して下さい。
