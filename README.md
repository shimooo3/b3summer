# b3summer  
### シミュレータ
* sim_gui.py　tkinterを使用した
### /predict
**生成された.csv,.txtは適宜必要な階層に配置してください**
#### 1, get_url.pyの実行  
* レースのurlを収集する  
* 生成されたcsvは2で使う 
#### 2, get_html.pyの実行  
* レース結果の表データを取得する
* 生成されたcsvは3で使う
#### 3, preprocess.ipynbの実行
* レース結果情報の前処理　カテゴリカル変数の作成、null処理.etc...
* jupyterの方が適宜修正や型確認でコードを記述しやすかった
* train.csvは4で使用、残りのcsvは5で使用
#### 4, model.pyの実行
* 着順を予測するモデル(lightgbm)を作成する
* 4位以下とそれ以外でデータの偏りが大きいためアンダーサンプリングを実行
* 生成されたlgb.txtは5で使用
#### 5, predict.pyの実行
* 任意パラメータで予測
* 馬名、騎手名は日本語入力、残りは半角数字で入力
* G1,G2レースが対象のため新馬、新騎手には非対応。3で生成したmap.csvを確認  
