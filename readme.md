# snake demo
オープンキャンパスなどのデモで見せる用のプログラム  
ラズパイ側のリポジトリ  
蛇に搭載されたラズパイにすでに入っているので、基本的に入れる必要はない  
ラズパイを初期化したり、壊れたりしたときにこれを入れる

## demo.py

### 使い方
1. ライブラリインストール
~~~
pip install -r requirements.txt
~~~

2. 実行
~~~
python control_snake.py
~~~

### 概要
UDPでPCから制御信号を受け取り、蛇を制御するプログラム