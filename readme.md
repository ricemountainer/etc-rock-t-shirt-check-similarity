# 毎日バンTチャレンジチェックツール

その日のバンTを以前着たことがあるかをチェックするツール

# 使い方

1. `./input/`配下にファイルを配置する(仮に`20240101.jpg`とする)
2. `python3 check.py 1.のファイル名`
3. `history.csv`に1.のファイルの内容を書き込む

※1.のファイルは処理後に自動で`./all`ディレクトリ配下に移動されます  
  
実行結果例:  

```shell
> python3 check.py test.jpg
/usr/local/lib/python3.8/dist-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/usr/local/lib/python3.8/dist-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ResNet50_Weights.IMAGENET1K_V1`. You can also use `weights=ResNet50_Weights.DEFAULT` to get the most up-to-date weights.
類似した画像が見つかりました。
ファイル名: ./all/20240617.jpg, 詳細:['ストレイテナー', 'ROCKSTEADY - Black', '0'], 類似度スコア: 0.8470852971076965
```

```shell
> python3 check.py test2.jpg
/usr/local/lib/python3.8/dist-packages/torchvision/models/_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
/usr/local/lib/python3.8/dist-packages/torchvision/models/_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=ResNet50_Weights.IMAGENET1K_V1`. You can also use `weights=ResNet50_Weights.DEFAULT` to get the most up-to-date weights.
類似した画像は見つかりませんでした。
```


# `history.csv`について

[拡張子を除外したファイル名]、[バンド名・フェス名等]、[Tシャツ名]、[メモ]の順で記述します。  
例:  

```CSV
20240616,MONOEYES,Between Black And Glay Tour,0
20240617,ストレイテナー,ROCKSTEADY - Black,0
20240618,ストレイテナー,BASE BALL T - Glay,0
...
```

- [拡張子を除外したファイル名]は例えば`20240617.jpg`なら`20240617`となります。例えばパーカーとか着る季節で`20241201_1.jpg`でTシャツ`20241201_2.jpg`でパーカーみたいな着回しする場合は`20241201_1`で1行、`20241201_2`で1行、合計2行になるように使うことを想定しています。
- [Tシャツ名]はわかる値がついていればなんでもいいですが過去に同じTシャツ着てたときにわかるように、同じTシャツの場合は同じ名前書いておくことをお勧めします。
- [メモ]は好きに使えるなんでもいい項目です(上の例は、Tシャツなら`0`、ロンTなら`1`、パーカーなら`2`みたいに使うことを想定してました)