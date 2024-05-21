import requests
from datetime import datetime
import numpy as np
import pandas as pd

HOST = 'https://api.meteo.lt/v1'
r = requests.get(HOST + '/places/vilnius/forecasts/long-term')
json = r.json()

column_names = [*json['forecastTimestamps'][0].keys()]
values_list = [[*item.values()] for item in json['forecastTimestamps']]

numpy_array = np.array(values_list)
dataset = pd.DataFrame(numpy_array, columns=column_names)
