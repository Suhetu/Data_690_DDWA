import streamlit as st

st.title("Continent-wise Yearly Temperature Trend")
st.sidebar.title("# Yearly Continent Analysis")
st.sidebar.markdown("This page provides yearly temperature trend of continent selected")

# Importing necessary libraries

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

# Reading in the dataset to a dataframe

df_country = pd.read_csv('GlobalLandTemperaturesBy_Country.csv')

df_country.dropna(inplace=True)

df_country['dt'] = pd.to_datetime(df_country.dt)

continents = ['Asia', 'Europe', 'South America', 'Africa', 'Antarctica', 'North America', 'Oceania']

df_continents = df_country[df_country['Country'].isin(continents)]
df_country = df_country[~df_country['Country'].isin(continents)]

df_continents.reset_index(inplace=True)
df_continents.drop(['index'], axis=1, inplace=True)

df_country.reset_index(inplace=True)
df_country.drop(['index'], axis=1, inplace=True)

df_continents['Year'] = df_continents['dt'].dt.year
df_continents = df_continents.groupby(['Country', 'Year'])['AverageTemperature'].mean().reset_index()

continent_list = ['Asia', 'Europe', 'South America', 'Africa', 'North America', 'Oceania']

cselect = st.radio(
    "Please select a continent: ",
    ('Asia', 'Europe', 'South America', 'Africa', 'North America', 'Oceania'))

x = list(df_continents[df_continents['Country'] == cselect]['Year'])
y = list(df_continents[df_continents['Country'] == cselect]['AverageTemperature'])

if st.button('Get Plot!'):
    st.write("Here's your plot...")
    fig1, ax = plt.subplots(constrained_layout=True, figsize=(10, 8))
    ax = plt.plot(x, y, label =cselect)
    plt.legend(loc ="upper left")
    plt.title(cselect + ' Average Temperatures')
    plt.xlabel('Year')
    plt.ylabel('Temperature (in C)')
    plt.grid()
    # plt.show()
    st.pyplot(fig=fig1)