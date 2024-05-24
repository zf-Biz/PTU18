#!/usr/bin/env python
# coding: utf-8

# ## Importing the libraries

# In[53]:


import requests
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ## json Request from API

# In[54]:


HOST = 'https://api.meteo.lt/v1'
r = requests.get(HOST+'/places/vilnius/forecasts/long-term')
json = r.json()


# In[55]:


time_stamp = 'Forecast_at_' + datetime.now().strftime("%Y_%m_%d_%H_%M") + '.csv'
print(time_stamp)


# ## Converting json to dataframe

# In[56]:


dataset = pd.DataFrame.from_dict(json['forecastTimestamps'])


# ## Checking for NaN values

# In[57]:


dataset.isnull().values.any()


# In[58]:


dataset.isnull().sum()


# ## Saving dataframe to .csv file

# In[59]:


dataset.to_csv(time_stamp, index=False)


# ## Plotting dataframe

# In[60]:


plt.plot(dataset['forecastTimeUtc'].index[:], dataset.iloc[:,1].values, color='black')
plt.scatter(dataset['forecastTimeUtc'].index[:], dataset.iloc[:,1].values, color='black')
plt.xlabel(dataset.iloc[0,0][0:-3] + " " + dataset.iloc[-1,0][0:-3])
plt.ylabel('Temperature (C)')
plt.show()


# ## Filtering dataframe by hour

# In[61]:


# data_by_hour = dataset[dataset['forecastTimeUtc'].str.contains('00:00:00')]


# In[62]:


# plt.plot(data_by_hour['forecastTimeUtc'].index[:56], data_by_hour['airTemperature'], color='red')
# plt.xlabel(dataset.iloc[0,0][0:11] + dataset.iloc[-1,0][0:10])
# plt.ylabel('Temperature (C)')
# plt.show()


# ## Splitting dataframe to X and y dataframes

# In[63]:


X = dataset.iloc[:, 3:].values
y = dataset.iloc[:,1].values


# ## Encoding categorical data

# In[64]:


from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [-1])], remainder='passthrough')
X = np.array(ct.fit_transform(X))


# ## Filling missing dataframe values

# In[65]:


from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values = np.nan, strategy = 'mean')
imputer.fit(X)
X = imputer.transform(X)


# ## Splitting the dataset into the Training set and Test set

# In[66]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state = 42)


# ## Training the Multilinear Regression model on the Training set

# In[67]:


from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)


# ## Visualising the Multilinear Regression results with dataframe results

# In[71]:


plt.scatter(dataset.index[0:len(y_test)], y_test, color = 'red')
plt.scatter(dataset.index[0:len(y_test)], regressor.predict(X_test), color = 'blue')
plt.plot(dataset.index[0:len(y_test)], y_test, color = 'red')
plt.plot(dataset.index[0:len(y_test)], regressor.predict(X_test), color = 'blue')
plt.title('Multilinear Regression')
plt.xlabel('Index')
plt.ylabel('Temperature (C)')
plt.show()


# ## Predicting the Test set results

# In[69]:


y_pred = regressor.predict(X_test)
np.set_printoptions(precision=2)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))


# ## Evaluating the Model Performance

# In[70]:


from sklearn.metrics import r2_score
r2_score(y_test, y_pred)


# In[ ]:




