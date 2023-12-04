import streamlit as st
import pandas as pd
import altair as alt 

df = pd.read_csv("data.csv")

st.bar_chart(data=df, x="BOROUGH", y="NUMBER OF PERSONS KILLED")

