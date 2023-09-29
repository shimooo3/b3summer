import matplotlib.pyplot as plt
import numpy as np

# 離散データ
discrete_data = [
    0, 100, 250, 300, 470, 450, 600, 700, 650, 900, 1000
]

# 連続データ
continuous_data = [
    0, 70, 190, 320, 500, 400, 650, 700, 600, 950, 1024
]

# 離散データのx座標
x_discrete = np.arange(len(discrete_data))

# 連続データをプロットするためのx座標
x_continuous = np.linspace(0, len(discrete_data) - 1, 100)

# 連続データを補完して曲線を生成
y_continuous_interp = np.interp(x_continuous, x_discrete, continuous_data)

# グラフ描画
plt.figure(figsize=(8, 6))
plt.plot(x_discrete, discrete_data, 'o-', label="離散データ (折れ線)", color="blue")
plt.plot(x_continuous, y_continuous_interp, '-', label="連続データ (補完曲線)", color="red")

# グラフにタイトルと軸ラベルを追加
plt.title("離散データと連続データのグラフ")
plt.xlabel("データポイント")
plt.ylabel("値")

# 凡例を表示
plt.legend()

# グラフを表示
plt.grid(True)
plt.show()
