SmArtBox機能の自動実行について
                                    Rev. 1.0   15/01/26 shiu

SmArtBoxの各機能は、Supervisor というプログラムのデーモン化を
行うサービスにて行っています。その使いかたについてメモ。

●supervisor関連
・supervisor 自体は自動起動の設定がされているので起動する必要はない。
　必要な場合は、下記。
　$ sudo supervisord

・プロセスの追加/変更(プロセス XXXXX を追加する場合)
　/etc/supervisor/conf.d/ 内にXXXXX.confファイルを追加
　(内容については、shutdownbutton.conf(付録 - 例1)などを参照)

・今どんなプロセスが動いているかプロセスの確認
　$ sudo supervisorctl status


●プロセスの起動/再起動/停止
　(shutdownbutton を例にして説明すると)

・起動
　$ sudo supervisorctl start shutdownbutton

・再起動
　$ sudo supervisorctl restart shutdownbutton

・停止
　$ sudo supervisorctl stop shutdownbutton

・追加
　$ sudo supervisorctl reread
　$ sudo supervisorctl add shutdownbutton



●付録

-例1 (shutdownbutton.conf)-----
[program:shutdownbutton]
command=sudo python /home/smartuser/bin/shutdownbutton/shutdownbutton.py --config=/home/smartuser/bin/shutdownbu
tton/shutdownbutton.conf
numprocs=1
autostart=true  ; autostart when supervisor died
autorestart=true ; autorestart when daemon died
user=hoge
redirect_stderr=true ;
stdout_logfile=/home/smartuser/var/shutdownbutton.log ;
-------------------------------

-EOF-