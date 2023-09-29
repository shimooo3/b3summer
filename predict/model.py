import pandas as pd
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from imblearn.under_sampling import RandomUnderSampler

df = pd.read_csv("data/train/train.csv")
df.drop(columns=['馬名', '騎手'], inplace=True)

x = df.drop('着順', axis=1)
y = df['着順']

# クラス0、1、2、3の各サンプル数
class_counts = [579, 579, 579, 579]

target_ratios = [4, 1, 1, 1]

# 各クラスに対する目標サンプル数を計算
target_samples = [count * ratio for count, ratio in zip(class_counts, target_ratios)]

# RandomUnderSamplerを初期化
under_sampler = RandomUnderSampler(sampling_strategy=dict(zip(range(4), target_samples)), random_state=0)
# under_sampler = RandomUnderSampler(sampling_strategy='auto', random_state=0)
x_resampled, y_resampled = under_sampler.fit_resample(x, y)
print(y_resampled.value_counts())

x_train, x_test, y_train, y_test = train_test_split(x_resampled, y_resampled, test_size=0.2, random_state=0)
train_data = lgb.Dataset(x_train, label=y_train)
test_data = lgb.Dataset(x_test, label=y_test)

params = {
    'objective': 'multiclass',
    'num_class': 4,
    'metric': 'multi_logloss',
    'verbose': 1,
    'max_bin': 300,
    'num_leaves': 63,
    'learnig_rate': 0.01
}

model = lgb.train(params, train_data, num_boost_round=100, valid_sets=[train_data, test_data],callbacks=[lgb.early_stopping(stopping_rounds=10)])

y_pred = model.predict(x_test)
y_pred_class = y_pred.argmax(axis=1)

accuracy = accuracy_score(y_test, y_pred_class)
print('Accuracy: ', accuracy)
conf_matrix = confusion_matrix(y_test, y_pred_class)
print('Confusion Matrix:\n', conf_matrix)
f1 = f1_score(y_test, y_pred_class, average='weighted')
print('F1-Score:', f1)

model.save_model('lgb.txt')

# import matplotlib.pyplot as plt
# plt.rcParams['font.family'] = 'MSGothic'
# lgb.plot_importance(model, importance_type='split', figsize=(10, 6))
# plt.show()