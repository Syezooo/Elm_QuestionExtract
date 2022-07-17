# アンケートトリミング自動化
第41回演奏会アンケート用トリミング自動化計画

---

# 0. 実装環境
* ubuntu18.04
* python3.8
* pillow9.0.1

・・・

#### フォルダ構成
```
├── README.md           本mdファイル
├── data/               pdfファイルを格納するフォルダ
├── src/                
│   └── trim.py         トリミングを行うコード
├── results/
│   ├── img/            pdfが1ページごとに分割されたファイルが格納されるフォルダ
│   └── outsputs/       トリミング結果を格納するフォルダ
│       ├── q1/         設問名をq1とした際（trim.pyで指定）に自動生成
│       ・
│       ・
│       ・
```

---

# 1. 実装方法
#### 1.1. dockerコンテナを読み込み（環境構築）

```
$ docker pull nvcr.io/nvidia/pytorch:22.06-py3
$ docker run --gpus "device=0" -it --rm --name [任意のコンテナ名] -v $PWD:/workspace/ -w /workspace/ nvcr.io/nvidia/pytorch:22.06-py3
```

※pytorchは絶対要らないけど大体のことができるコンテナなので利用

#### 1.2. data/にトリミングしたいアンケートのpdfファイルを格納し、ページごとに画像として分割

```
$ apt-get update
$ apt-get install poppler-utils
$ pdftoppm -png <input.pdf> /workspace/results/img/
```


#### 1.3. src/trim.pyの30行目以降でトリミング領域を指定
```python
# 保存先パスとトリミング位置（アンケートごとに変わる）を指定
    ### q1（1曲目）###
    trim_question(img_path, save_path_q1, 0, 370, 1074, 620, outtype)

    ### q2（2曲目）###
    trim_question(img_path, save_path_q2, 0, 600, 1074, 840, outtype)

    ### q3（3曲目）###
    trim_question(img_path, save_path_q3, 0, 820, 1074, 1050, outtype)

    ### q4（その他お気づきの点など）###
    trim_question(img_path, save_path_q4, 0, 1030, 1074, 1200, outtype)

    ### q5（個人情報）###
    if args.privacy == 'ON':
        trim_question(img_path, save_path_q5, 0, 1180, 1074, 1520, outtype)
```

#### 1.4. src/trim.pyのoptions詳細を指定しながらスクリプト実行
```python
# オプション指定
def Options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--outtype', type=str, default='pdf', help='保存する拡張子を指定')
    parser.add_argument('--img_path', type=str, default='/workspace/results/img/*' , help='pdf→imageの変換で保存された画像が格納されたパスを指定')
    parser.add_argument('--privacy', type=str, default='OFF', help='個人情報をトリミングするか否か。ONにするとq5として保存される。')
    return parser.parse_args()
```
スクリプト実行例

`$ python3 /workspace/src/trim.py --outtype pdf --img_path /workspace/results/img/ --privacy OFF`

標準出力（上記スクリプト実行時）
```
Processing /workspace/results/img/-217.png to /workspace/results/outputs/q1/: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 217/217 [00:04<00:00, 52.47it/s]
Processing /workspace/results/img/-217.png to /workspace/results/outputs/q2/: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 217/217 [00:04<00:00, 53.09it/s]
Processing /workspace/results/img/-217.png to /workspace/results/outputs/q3/: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 217/217 [00:04<00:00, 53.95it/s]
Processing /workspace/results/img/-217.png to /workspace/results/outputs/q4/: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 217/217 [00:03<00:00, 55.45it/s]
```

---

# 2. 今後の懸念点

* スクリプト分割用にアンケートフォームを作っていくとよいかも
* 最終出力はどんな形がよいか？全員分が結合されたpdfなのか。