# 概要

標準入力からIPv4アドレスのリストを読み込み、whoisのCIDR,NetName毎に分類して統計を表示する。

WebサーバーにBot等からの大量のアクセスがあった際に、アクセス元を速やかに見つけたい時に使用できる。

# 使い方
    python3 topnetblock.py < iplist.txt

以下のようなIPv4アドレスの一覧を標準入力から渡す。

    xxx.xxx.xxx.xxx
    yyy.yyy.yyy.yyy

Apache/NginxのアクセスログからIPアドレスのリストを作成するには、以下のようにして作成できる。通常、ログはかなり大きいので、ログファイルから調べたい時間帯の部分を抜き出してから処理した方がよい。


    awk '{print $1}' access_log > iplist.txt


netstatから現在接続中のクライアントのIPアドレス一覧を取得する例。


    netstat -tn | tail -n+3 | awk '{print $5}' | sed 's/:.*$//' > iplist.txt

IPv4アドレスの一覧を渡してコマンドを実行すると、以下のようにネットワークアドレス、ネットワーク名ごとの出現回数を出力する。

Botなどからの大量アクセスがあった場合、アクセス元のIPを分散させていたとしても、ネットワークアドレスは偏るので、アクセス拒否の設定を行う際の情報収集に役立てることができる。


    Founded netblocks
    172.106.0.0/15: 21
    104.149.0.0/16: 9
    23.228.192.0/18: 6
    <略>
    
    Founded netnames
    PSYCHZ-NETWORKS: 48
    VPLSNET: 7
    APNIC-27: 6
    <略>

# 必要要件

- Python3
- netaddrモジュール

# 制限

対応しているのはIPv4アドレスのみ。

whoisが返す内容はフォーマットがまちまちなので、CIDR、NetNameを取得できないケースもある。

