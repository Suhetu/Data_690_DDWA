import streamlit as st

st.title("Project 2 - Understanding Earthly Temperature 🌏")
st.sidebar.header("# Intro Page")
st.sidebar.markdown("This page gives an intro to this WebApp")

st.image("https://spaceplace.nasa.gov/gallery-earth/en/ISS_earth.en.jpg")

st.header("Project Motivation:")
st.subheader("In view of the global warming which is affecting our planet Earth, this project aims to help us understand how we're being affected in different parts of Earth and Earth as a whole. We will notice some trends and will forecast Earth's temperature over the coming years.")
st.write("Navigate to different pages on the sidebar for the following:")
st.write("1. This widget shows the temperature trend of different continents over the years. We can select which continent trend we want to view and click 'Get Plot' to get the plot.")
st.write("2. This widget can be used to compare temperatures of different countries at different years. It consists of two sliders using which we can select years, a button which is clicked to get visualizations and two interactive choropleth maps at years selected from sliders.")
st.write("3. This widget consists of time series forecasting which tells us the average land temperature of Earth over the past years and also predicts into the future until 2105. It contains a slider to select year for which we want to see the average land temperature of Earth and a button which updates the visualization. On each update, the marker on the graph will change and point towards the updated information requested.")

st.caption("Thank You!")