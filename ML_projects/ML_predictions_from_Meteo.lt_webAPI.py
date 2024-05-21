import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HOST = 'https://api.meteo.lt/v1'
r = requests.get(HOST + '/places/vilnius/forecasts/long-term')
json = r.json()

dataset = pd.DataFrame.from_dict(json['forecastTimestamps'])

dataset.to_csv("Forecast_at_2024_05_21_15_00.csv", index=False)

plt.plot(dataset['forecastTimeUtc'].index[:56], dataset.iloc[:56, 1].values, color='red')
plt.xlabel(dataset.iloc[0, 0] + " " + dataset.iloc[-1, 0])
plt.ylabel('Temperature (C)')
plt.show()
