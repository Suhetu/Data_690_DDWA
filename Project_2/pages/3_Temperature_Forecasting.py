import streamlit as st

st.title("Temperature Rolling Average Analysis and Forecasting")
st.sidebar.title("# Temperature Observation and Forecasting")
st.sidebar.markdown("This page observes previous temperature trend of Earth and forecasts the same")

# Importing necessary libraries

import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.deterministic import DeterministicProcess

temperatures = pd.read_csv('GlobalTemperatures.csv')

temperatures['Date'] = pd.to_datetime(temperatures.dt, format='%Y-%d-%m')
temperatures['Year'] = temperatures['Date'].dt.year
temperatures['Date'] = temperatures['Date'].map(dt.datetime.toordinal)
# df = temperatures.groupby('Year')['LandAverageTemperature'].mean().reset_index()
average_temperature = temperatures.groupby('Year').mean()['LandAverageTemperature']
ynew = average_temperature.copy()

dp = DeterministicProcess(index=ynew.index, order=3)
X = dp.in_sample()
X_fore = dp.out_of_sample(steps=90)

model = LinearRegression()
model.fit(X, ynew)

y_pred = pd.Series(model.predict(X), index=X.index)
y_fore = pd.Series(model.predict(X_fore), index=X_fore.index)

yearslider = st.slider(label = 'Select Year: ', min_value=1750, max_value=2105, value=2022)
marker_on_static = 2080
marker_on = yearslider
arrowprops={'arrowstyle': '-', 'ls':'--'}

if st.button('Get Plot!'):
        fig, ax = plt.subplots(constrained_layout=True, figsize=(14, 8))
        ax = ynew.plot(alpha=0.5, title="Average Land Temperature", ylabel="Land Temperature")
        ax = y_pred.plot(ax=ax, linewidth=3, label="Trend", color='C0')
        ax = y_fore.plot(ax=ax, linewidth=3, label="Trend Forecast", color='C3')
        if marker_on > 2015:
            plt.plot(marker_on, y_fore[marker_on], marker="*", markersize=20, markeredgecolor="C0", markerfacecolor="black")
            plt.annotate("Requested Point", (marker_on, y_fore[marker_on]))
            plt.annotate(str(marker_on), xy=(marker_on, y_fore[marker_on]), xytext=(marker_on, 0), 
             textcoords=plt.gca().get_xaxis_transform(),
             arrowprops=arrowprops,
             va='top', ha='center')
            plt.annotate(str(y_fore[marker_on]), xy=(marker_on,y_fore[marker_on]), xytext=(0, y_fore[marker_on]), 
                     textcoords=plt.gca().get_yaxis_transform(),
                     arrowprops=arrowprops,
                     va='center', ha='right')
        else:
            plt.plot(marker_on, y_pred[marker_on], marker="*", markersize=20, markeredgecolor="C3", markerfacecolor="black")
            plt.annotate("Requested Point", (marker_on, y_pred[marker_on]))
            plt.annotate(str(marker_on), xy=(marker_on, y_pred[marker_on]), xytext=(marker_on, 0), 
             textcoords=plt.gca().get_xaxis_transform(),
             arrowprops=arrowprops,
             va='top', ha='center')
            plt.annotate(str(y_pred[marker_on]), xy=(marker_on,y_pred[marker_on]), xytext=(0, y_pred[marker_on]), 
                     textcoords=plt.gca().get_yaxis_transform(),
                     arrowprops=arrowprops,
                     va='center', ha='right')
        ax.legend()
        st.pyplot(fig=fig)

