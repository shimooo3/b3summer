# ライブラリのインポート
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import random
import time
import warnings
warnings.filterwarnings('ignore')

# allからnum分だけランダムに選択する関数
def random_select(all, num):
    list = []
    for a in random.sample(all, num):
        list.append(a)
    return list

#2次元配列allのnum列を1~size行を抽出する関数
def append_2Dlist(all, num, size):
    list = []
    for a in range(size):
        list.append(all[a][num])
    return list

# 所持金を入力する
money = input("所持金を入力して下さい\n所持金[円]: ")
start_money = money
print("")

# 馬情報を設定する
horse_number = [0,1,2,3,4]
horse_name = ['horseA','horseB','horseC', 'horseD', 'horseE']
horse_power = [1, 2, 3, 4, 5]
tension = ['best','normal','worst', 'high', 'normal', 'low']

# レースの長さを設定する
length = 1600

# 馬情報の組み合わせを決定する(重複無しランダム)
lane_size = len(horse_number)
horse_info = []
horse_info.append(random_select(horse_number, lane_size))
horse_info.append(random_select(horse_name, lane_size))
horse_info.append(random_select(horse_power, lane_size))
horse_info.append(random_select(tension, lane_size))
print(len(horse_info))

# レーンに配置する
horse_info_size = len(horse_info)
lane_info = []
for a in range(lane_size):
    lane_info.append(append_2Dlist(horse_info, a, horse_info_size))

# 出馬表を出力する
print("--出馬表を表示します--")
print("lane", " num", "name", "power", "tension")
for a in range(lane_size):
    print('lane'+str(a+1)+":",end=" ")
    for b in range(horse_info_size):
        print(lane_info[a][b], end=" ")
        if b == horse_info_size-1:
            print("")
print("----------------------\n")

# オッズを出力する
odds = []
for a in range(lane_size):
    odds.append(round(random.uniform(1.01, 5.00), 2))
print("--オッズを表示します--")
for a in range(lane_size):
    print('lane'+str(a+1)+":",end=" ")
    print(odds[a])
print("----------------------\n")

# 予想する
print("予想した馬番号を入力して下さい")
predict = int(input("馬番号: "))

print("賭ける金額を入力して下さい")
stakes = int(input("賭け金[円]: "))
money = int(money)-int(stakes)
print("")

# コースを作成する
length_lest = []
for a in range(lane_size):
    length_lest.append(length)

# レースを開始する
print("レースを開始します")
goal_min = 1
race_graph_df = pd.DataFrame(columns=horse_info[0])

race_finish = False
# 1位が決まるまで繰り返す
while(race_finish == False):
    for a in range(lane_size):
        
        #ゴールしているレーンはスキップ
        #tensionに応じて進む距離を変える
        if length_lest[a] > 0:  #ゴールしていない場合のみ進行
            tension_factor = 1.0
            if horse_info[3][a] == 'best':
                tension_factor = 1.2
            elif horse_info[3][a] == 'high':
                tension_factor = 1.1
            elif horse_info[3][a] == 'low':
                tension_factor = 0.9
            elif horse_info[3][a] == 'worst':
                tension_factor = 0.8

            #距離を減算（tensionに基づいて乗数を適用）
            length_lest[a] = length_lest[a] - round(random.uniform(1, 10) * tension_factor)
            #horse_powerに応じて進む距離を増やす
            length_lest[a] = length_lest[a] - horse_info[2][a]

        #グラフ用にデータフレームとして保存しておく
        df_race = pd.DataFrame(data=[length_lest], columns=horse_info[0])
        race_graph_df = pd.concat([race_graph_df, df_race], ignore_index=True)

        # ゴールした時
        if (length_lest[a] <= 0) and (goal_min > length_lest[a]):
            win_lane = a
            goal_min = length_lest[a]
            race_finish = True

# レース結果を表示する
print("--レース結果--")
print("1着: "+str(lane_info[win_lane][0]))
print("--------------")

print(race_graph_df)

# レースのグラフを表示する
cmap = plt.get_cmap('tab10')
plt.figure(figsize=[9,5])
plt.plot(race_graph_df)
plt.title("Race Result")
plt.xlabel("Time")
plt.ylabel("Length Lest")
plt.show()

# 金額変動を判定する
if predict == lane_info[win_lane][0]:
    money = int(money + stakes*odds[win_lane])
print("結果: "+str(start_money)+" → "+str(money))

# 終了処理
print("3秒後に終了します")
time.sleep(3)
os.system('cls')