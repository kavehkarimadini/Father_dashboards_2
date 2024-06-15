import pandas as pd
# import string
import streamlit as st
import plotly.express as px

eucladian_file = st.file_uploader("Select Your Local CSV file")
if eucladian_file is None:
    st.stop()
else:
    eucladian_df = pd.read_csv(eucladian_file)
# eucladian_df = load_data_yearly()
eucladian_df.index = eucladian_df.columns
fig_heatmap = px.imshow(eucladian_df)
st.plotly_chart(fig_heatmap)