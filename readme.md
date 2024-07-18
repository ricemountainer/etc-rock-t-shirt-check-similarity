# 毎日バンTチャレンジチェックツール

その日のバンTを以前着たことがあるかをチェックする個人用のツール。私自身の毎日バンTチャレンジは[ここのTwitterのPOSTのツリー](https://x.com/ricemountainer/status/1802313798545494341)でやっています。

# 使い方

1. 同階層にTシャツ画像ファイルを配置する(仮に`20240101.jpg`とする)
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

[ファイル名]、[バンド名・フェス名等]、[Tシャツ名]、[メモ]の順で記述します。  
例:  

```CSV
20240616.jpg,MONOEYES,Between Black And Glay Tour,0
20240617.jpg,ストレイテナー,ROCKSTEADY - Black,0
20240618.jpg,ストレイテナー,BASE BALL T - Glay,0
...
```

- [Tシャツ名]はわかる値がついていればなんでもいいですが過去に同じTシャツ着てたときにわかるように、同じTシャツの場合は同じ名前書いておくことをお勧めします。
- [メモ]は好きに使えるなんでもいい項目です(上の例は、Tシャツなら`0`、ロンTなら`1`、パーカーなら`2`みたいに使うことを想定してました)

# 集計

`history.csv`の中の集計する項目の順番を`awk`の`count`の引数に与えるだけです。例えばバンド別集計なら（バンドの位置が2番目なので）

```shell
> awk -F, '{count[$2]++} END {for (b in count) print count[b], b}' "history.csv" | sort -nr
26 ストレイテナー
4 Nothing's Carved In Stone
1 その他
1 MONOEYES
1 9mm Parabellum Bullet
```

となります。Tシャツ別集計なら（Tシャツの位置が3番目なので）`awk -F, '{count[$3]++} END {for (b in count) print count[b], b}' "history.csv" | sort -nr`になります。
