# Artificial Neural Network

# Importing the libraries

import requests
from datetime import datetime
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# json Request from API:
# HOST = 'https://api.meteo.lt/v1'
# r = requests.get(HOST + '/places/vilnius/forecasts/long-term')
# json = r.json()

# Converting json to dataframe:
# dataset = pd.DataFrame.from_dict(json['forecastTimestamps'])

# Saving json as .csv file:
# time_stamp = 'Forecast_at_' + datetime.now().strftime("%Y_%m_%d_%H_%M") + '.csv'
# dataset.to_csv(time_stamp, index=False)

# Data Preprocessing

dataset = pd.read_csv('Forecast_at_2024_06_13_13_44.csv')

X = dataset.iloc[:, 3:].values
y = dataset.iloc[:, 1].values

# Encoding the Independent Variable:

ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [-1])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

# Taking care of missing data:

if dataset.isnull().values.any():
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    imputer.fit(X)
    X = imputer.transform(X)

X = np.asarray(X).astype(np.float32)
y = np.asarray(y).astype(np.float32)
# Splitting the dataset into the Training set and Test set:

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

# Building the ANN
# Initializing the ANN:

ann = tf.keras.Sequential()

# Adding the input layer and the first hidden layer:

ann.add(tf.keras.layers.Dense(units=6, activation='relu'))

# Adding the second hidden layer:

ann.add(tf.keras.layers.Dense(units=6, activation='relu'))

# Adding the output layer:

ann.add(tf.keras.layers.Dense(units=1))

# Training the ANN
# Compiling the ANN:

ann.compile(optimizer='adam', loss='mean_squared_error')

# Training the ANN model on the Training set:

ann.fit(X_train, y_train, batch_size=1, epochs=100)

# Predicting the results of the Test set:

y_pred = ann.predict(X_test)

# Evaluating the Model Performance:

r2_score = r2_score(y_test, y_pred)
print(r2_score)

# Visualising the Artificial Neural Network results with dataframe results:

plt.plot(range(0, len(y_test)), y_test, color='red')
plt.scatter(range(0, len(y_test)), y_test, color='red', label='Test values')
plt.plot(range(0, len(y_pred)), y_pred, color='blue')
plt.scatter(range(0, len(y_pred)), y_pred, color='blue', label='Predicted values')
plt.title(str(round(r2_score, 3)))
plt.title('Artificial Neural Network' + '\n' + 'Mean square root: ' + str(round(r2_score, 3)))
plt.xlabel('Index')
plt.ylabel('Temperature (C)')
plt.grid()
plt.legend()
plt.show()
