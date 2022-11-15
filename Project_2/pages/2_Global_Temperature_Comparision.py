import streamlit as st

st.title("Global Temperature Comparision")
st.sidebar.title("# Global Temperature Comparision")
st.sidebar.markdown("This page enables us to compare temperatures of globe on two years")

# Importing necessary libraries

import pandas as pd
import plotly.graph_objects as go
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

intslider1 = st.slider(label = 'Select Year 1: ', min_value=1750, max_value=2015, value=1912)
intslider2 = st.slider(label = 'Select Year 2: ', min_value=1750, max_value=2015, value=2012)

df_codes = pd.read_csv('countries_codes_and_coordinates.csv')
df_codes['Alpha-3 code'] = df_codes['Alpha-3 code'].str.replace('"', '').replace(' ', '')
df_codes['Numeric code'] = df_codes['Numeric code'].str.replace('"', '').replace(' ', '')
df_codes = df_codes[['Country', 'Alpha-3 code', 'Numeric code']]

df_country = df_country.merge(df_codes, on='Country')
df_country['Year'] = df_country['dt'].dt.year
df_country = df_country.groupby(['Country', 'Year', 'Alpha-3 code', 'Numeric code'])['AverageTemperature'].mean().reset_index()
df_country['Alpha-3 code'] = df_country['Alpha-3 code'].str.replace(' ', '')

df1 = df_country.query('Year=='+str(intslider1))
fig1 = go.Figure(data=go.Choropleth(
            locations = df1['Alpha-3 code'],
            z = df1['AverageTemperature'],
            text = df1['Country'],
            colorscale = 'matter',
            autocolorscale=False,
            reversescale=True,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_title = 'Average Temperature',
        ))

df2 = df_country.query('Year=='+str(intslider2))
fig2 = go.Figure(data=go.Choropleth(
            locations = df2['Alpha-3 code'],
            z = df2['AverageTemperature'],
            text = df2['Country'],
            colorscale = 'matter',
            autocolorscale=False,
            reversescale=True,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_title = 'Average Temperature',
        ))

if st.button('Get Plot!'):
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

