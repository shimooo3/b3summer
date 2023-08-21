import pandas as pd
import lightgbm as lgb

model = lgb.Booster(model_file='data/model/lgb.txt')
horse_name = pd.read_csv('data/train/horse_number_mapping.csv')
jockey_name = pd.read_csv('data/train/jockey_number_mapping.csv')

#数値かどうかをチェックする
def is_numeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
def predict(data):
    prediction = model.predict(data)
    predicted_rank = int(prediction.argmax())

    print(data)
    print('----------------------------------')
    if predicted_rank > 0:
        print(f"予想順位: {predicted_rank}")
    else:
        print('4位以下です')
    print('----------------------------------')

mode = int(input('ダミー:0, 予想:1 : '))

while True:
    if mode == 0:
        data = pd.DataFrame({
            '枠番': [5],
            '馬名': [1],
            '斤量': [55],
            '騎手': [1],
            '人気': [100],
            '性別': [1],
            '年齢': [5]
        })
        predict(data)        
        break
    else:
        # 馬名の入力
        while True:
            horse_input = input('馬名を入力してください: ')
            if horse_input in horse_name[horse_name.columns[0]].values:
                row = horse_name[horse_name[horse_name.columns[0]] == horse_input]
                horse_num = row.iloc[0,1]
                break
            else:
                print('もう一度入力してください')

        # 騎手の入力
        while True:
            jockey_input = input('騎手を入力してください: ')
            if jockey_input in jockey_name[jockey_name.columns[0]].values:
                row = jockey_name[jockey_name[jockey_name.columns[0]] == jockey_input]
                jockey_num = row.iloc[0,1]
                break
            else:
                print('もう一度入力してください')

        # 数値データの入力
        while True:
            wakuban = input('枠番を入力してください: ')
            weight = input('斤量を入力してください: ')
            popular = input('人気を入力してください: ')
            gender = input('性別を牡:0, 牝:1で入力してください: ')
            age = input('年齢を数字で入力してください: ')

            if is_numeric(wakuban) and is_numeric(weight) and is_numeric(popular) and is_numeric(gender) and is_numeric(age):
                wakuban = float(wakuban)
                weight = float(weight)
                popular = float(popular)
                gender = float(gender)
                age = float(age)
                break
            else:
                print('入力が正しくありません。数値データを入力してください。')

        # 予測
        data = pd.DataFrame({
            '枠番': [wakuban],
            '馬名': [horse_num],
            '斤量': [weight],
            '騎手': [jockey_num],
            '人気': [popular],
            '性別': [gender],
            '年齢': [age]
        })
        predict(data)
        yn = input('別のデータを試しますか y/n: ')
        
        if yn == 'n':
            print('終了します')
            break
        else:
            print('続けます')
            continue
        
