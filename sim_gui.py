import tkinter as tk
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

money = 0
predict = 0
stakes = 0

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

def display_race():
    global money
    output_text.delete("1.0", tk.END)  # Clear previous output
    money =int(money_entry.get())  # Get the input from the entry widget
    try:
        start_money = money
    except ValueError:
        output_text.insert(tk.END, "Invalid input. Please enter a valid amount.\n")
        return

    # 馬情報のリスト（仮のデータ）
    horse_number = [0, 1, 2, 3, 4]
    horse_name = ['horseA','horseB','horseC', 'horseD', 'horseE']
    horse_power = [1, 2, 3, 4, 5]
    tension = ['best','normal','worst', 'high', 'normal', 'low']

    lane_size = len(horse_number)
    horse_info = []
    horse_info.append(random_select(horse_number, lane_size))
    horse_info.append(random_select(horse_name, lane_size))
    horse_info.append(random_select(horse_power, lane_size))
    horse_info.append(random_select(tension, lane_size))

    horse_info_size = len(horse_info)
    lane_info = []
    for a in range(lane_size):
        lane_info.append(append_2Dlist(horse_info, a, horse_info_size))
    
    output_text.insert(tk.END, "所持金: {}円\n".format(start_money))    
    # Display the race information
    output_text.insert(tk.END, "--出馬表を表示します--\n")
    output_text.insert(tk.END, "lane num name power tension\n")
    for a in range(lane_size):
        output_text.insert(tk.END, 'lane' + str(a + 1) + ": ")
        for b in range(horse_info_size):
            output_text.insert(tk.END, str(lane_info[a][b]) + " ")
        output_text.insert(tk.END, "\n")
    output_text.insert(tk.END, "----------------------\n")
    
    odds = []
    for a in range(lane_size):
        odds.append(round(random.uniform(1.01, 5.00), 2))
    output_text.insert(tk.END, "--オッズを表示します--\n")
    for a in range(lane_size):
        output_text.insert(tk.END, 'lane' + str(a + 1) + ": ")
        output_text.insert(tk.END, str(odds[a]) + "\n")
    output_text.insert(tk.END, "----------------------\n")
    
    predict_label = tk.Label(root, text="予想する馬番号:")
    predict_label.pack()
    predict_entry = tk.Entry(root)
    predict_entry.pack()

    # Entry widget for placing stakes
    stakes_label = tk.Label(root, text="賭ける金額[円]:")
    stakes_label.pack()
    stakes_entry = tk.Entry(root)
    stakes_entry.pack()
    
    def start_race():
        global win_lane, goal_min, start_money, predict, stakes, money
        predict = int(predict_entry.get())
        stakes = int(stakes_entry.get())
        output_text.insert(tk.END, "賭けた馬番号: {}\n".format(predict))
        output_text.insert(tk.END, "賭け金額: {}円\n".format(stakes))
        output_text.insert(tk.END, "----------------------\n")
        win_lane = 0
        goal_min = float('inf')
        length = 1600
        length_lest = []
        for a in range(lane_size):
            length_lest.append(length)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_ylim(-1, lane_size)
        ax.set_xlim(0, length)
        ax.set_yticks(range(lane_size))
        ax.set_yticklabels(horse_name)
        ax.set_xlabel("Remaining Distance")
        
        bars = ax.barh(range(lane_size), length_lest, tick_label=horse_name)
        
        def update(frame):
            global win_lane, goal_min  # グローバル変数を使用することを明示
            
            for i in range(lane_size):
                if length_lest[i] > 0:
                    tension_factor = 1.0
                    if horse_info[3][i] == 'best':
                        tension_factor = 1.2
                    elif horse_info[3][i] == 'high':
                        tension_factor = 1.1
                    elif horse_info[3][i] == 'low':
                        tension_factor = 0.9
                    elif horse_info[3][i] == 'worst':
                        tension_factor = 0.8

                    length_lest[i] -= round(random.uniform(1, 10) * tension_factor)
                    length_lest[i] -= horse_info[2][i]

                bars[i].set_width(length - length_lest[i])
                
                if min(length_lest) <= 0:
                    ani.event_source.stop()

                if (length_lest[i] <= 0) and (goal_min > length_lest[i]):
                    win_lane = i
                    goal_min = length_lest[i]

            return bars
        
        ani = FuncAnimation(fig, update, frames=None, blit=True, interval=10)
        plt.title("Race Animation")
        plt.ylabel("Horses")
        plt.xlabel("Remaining Distance")
        plt.show()

        plt.close()

        horse_num = length_lest.index(min(length_lest))
        if horse_num == 0:
            win_name = "horseA"
        elif horse_num == 1:
            win_name = "horseB"
        elif horse_num == 2:
            win_name = "horseC"
        elif horse_num == 3:
            win_name = "horseD"
        else:
            win_name = "horseE"
        # Display race result and update money
        output_text.insert(tk.END, "--レース結果--\n")
        output_text.insert(tk.END, "1着: " + win_name + "\n")
        output_text.insert(tk.END, "--------------\n")

        if predict == lane_info[win_lane][0]:
            money += int(stakes * odds[win_lane])
        start_money = money
        money -= stakes
        output_text.insert(tk.END, "結果: "+str(start_money)+" → "+str(money)+ "\n")
        output_text.insert(tk.END, "----------------------\n")
    
    # Button to place the start_race
    start_race_button = tk.Button(root, text="レースを開始", command=start_race)
    start_race_button.pack()
    
               

# 馬情報を設定する
horse_number = [0,1,2,3,4]
horse_name = ['horseA','horseB','horseC', 'horseD', 'horseE']
horse_power = [1, 2, 3, 4, 5]
tension = ['best','normal','worst', 'high', 'normal', 'low']

lane_size = len(horse_number)
horse_info = []
horse_info.append(random_select(horse_number, lane_size))
horse_info.append(random_select(horse_name, lane_size))
horse_info.append(random_select(horse_power, lane_size))
horse_info.append(random_select(tension, lane_size))

horse_info_size = len(horse_info)
lane_info = []
for a in range(lane_size):
    lane_info.append(append_2Dlist(horse_info, a, horse_info_size))

# Tkinter GUI
root = tk.Tk()
root.title("競馬シミュレータ")

# Entry widget for money input
money_label = tk.Label(root, text="所持金[円]:")
money_label.pack()
money_entry = tk.Entry(root)
money_entry.pack()

# Button to display the race information
display_button = tk.Button(root, text="レース情報", command=display_race)
display_button.pack()

# Text widget for displaying the race information
output_text = tk.Text(root)
output_text.pack()

root.mainloop()
