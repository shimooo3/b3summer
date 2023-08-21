import pandas as pd
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from sklearn.metrics import accuracy_score
from imblearn.under_sampling import RandomUnderSampler

df = pd.read_csv("data/train/train.csv")

categorical = ['馬名', '騎手']
x = df.drop('着順', axis=1)
y = df['着順']

# アンダーサンプリングを行う
under_sampler = RandomUnderSampler(sampling_strategy='auto', random_state=0)
x_resampled, y_resampled = under_sampler.fit_resample(x, y)

x_train, x_test, y_train, y_test = train_test_split(x_resampled, y_resampled, test_size=0.2, random_state=0)
train_data = lgb.Dataset(x_train, label=y_train, categorical_feature=categorical)
test_data = lgb.Dataset(x_test, label=y_test, categorical_feature=categorical)

params = {
    'objective': 'multiclass',
    'num_class': 4,
    'metric': 'multi_logloss',
    'verbose': 1
}

model = lgb.train(params, train_data, num_boost_round=100, valid_sets=[train_data, test_data], early_stopping_rounds=10)

y_pred = model.predict(x_test)
y_pred_class = y_pred.argmax(axis=1)

accuracy = accuracy_score(y_test, y_pred_class)
print('Accuracy: ', accuracy)

model.save_model('lgb.txt')