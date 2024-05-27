import requests
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

regressor = LinearRegression()
from sklearn.metrics import r2_score

# json Request from API:
HOST = 'https://api.meteo.lt/v1'
r = requests.get(HOST + '/places/vilnius/forecasts/long-term')
json = r.json()

# Converting json to dataframe:
dataset = pd.DataFrame.from_dict(json['forecastTimestamps'])

# Saving json as .csv file:
time_stamp = 'Forecast_at_' + datetime.now().strftime("%Y_%m_%d_%H_%M") + '.csv'
dataset.to_csv(time_stamp, index=False)
print(time_stamp)

# Splitting dataframe to X and y dataframes:
X = dataset.iloc[:, 3:].values
y = dataset.iloc[:, 1].values

# Encoding categorical data:
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [-1])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

# Checking for NaN values, if there are any, replace them with mean values:
if dataset.isnull().values.any():
    # Filling missing dataframe values:
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    imputer.fit(X)
    X = imputer.transform(X)

# Splitting the dataset into the Training set and Test set:
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# ## Training the Multilinear Regression model on the Training set:
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Predicting the Test set results:
y_pred = regressor.predict(X_test)
np.set_printoptions(precision=2)
print(np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), 1))

# Evaluating the Model Performance:
print(r2_score(y_test, y_pred))

# Visualising the Multilinear Regression results against dataframe values:
plt.scatter(dataset.index[0:len(y_test)], y_test, color='red')
plt.scatter(dataset.index[0:len(y_test)], y_pred, color='blue')
plt.plot(dataset.index[0:len(y_test)], y_test, color='red', label='Test values')
plt.plot(dataset.index[0:len(y_test)], y_pred, color='blue', label='Predicted values')
plt.title(f'Decision Tree Regression\nr^2={round(r2_score(y_test, y_pred), 3)}')
plt.xlabel('Index')
plt.ylabel('Temperature (C)')
plt.grid(True)
plt.legend()
plt.show()
