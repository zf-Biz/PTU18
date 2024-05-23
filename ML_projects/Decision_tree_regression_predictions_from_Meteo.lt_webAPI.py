import requests
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

HOST = 'https://api.meteo.lt/v1'
r = requests.get(HOST + '/places/vilnius/forecasts/long-term')
json = r.json()

dataset = pd.DataFrame.from_dict(json['forecastTimestamps'])

time_stamp = datetime.now()
dataset.to_csv(f'Forecast_at_{time_stamp.strftime("%Y_%m_%d_%H_%M")}.csv', index=False)

plt.plot(dataset['forecastTimeUtc'].index[:], dataset.iloc[:, 1].values, color='black')
plt.scatter(dataset['forecastTimeUtc'].index[:], dataset.iloc[:, 1].values, color='red')
plt.xlabel(dataset.iloc[0, 0][0:-3] + " " + dataset.iloc[-1, 0][0:-3])
plt.ylabel('Temperature (C)')
plt.show()

# data_by_hour = dataset[dataset['forecastTimeUtc'].str.contains('00:00:00')]
# plt.plot(data_by_hour['forecastTimeUtc'].index[:56], data_by_hour['airTemperature'], color='red')
# plt.xlabel(dataset.iloc[0,0][0:11] + dataset.iloc[-1,0][0:10])
# plt.ylabel('Temperature (C)')
# plt.show()

X = dataset.iloc[:, 3:].values
y = dataset.iloc[:, 1].values

ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [-1])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

regressor = DecisionTreeRegressor(random_state=0)
regressor.fit(X_train, y_train)

plt.scatter(dataset.index[0:len(y_test)], y_test, color='red')
plt.plot(dataset.index[0:len(y_test)], regressor.predict(X_test), color='blue')
plt.title('Truth or Bluff (Decision Tree Regression)')
plt.xlabel('Index')
plt.ylabel('Temperature')
plt.show()

print(predict(X_test))
print(y_test)
