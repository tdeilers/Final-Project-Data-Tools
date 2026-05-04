import streamlit as st
import requests
import json
import time
import datetime
import pandas as pd
import plotly.express as px

df = pd.read_csv("masterdata.csv")





print(df)

st.title("My First Chart")
#how do i add labels and stuff?
#nonfarm empoyment
nonfarmfig = px.line(df[df["series_id"]=="CES0000000001"], x = "date", y = "value", title = "Nonfarm Employment")
#unemployment rate, y axis is unemployment rate
unempfig = px.line(df[df["series_id"]=="LNS14000000"], x = "date", y = "value", title = "Unemployment Rate", labels = {"value": "Unemployment %", "date": "Date"}, template = "plotly_dark" )
unempfig.update_yaxes(range=[0,100],ticksuffix="%")
# labor force participation
lbrfig = px.line(df[df["series_id"]=="LNS11300000"], x = "date", y = "value", title = "Labor Force Statistics", labels= {"value": "Unemployment %", "date": "Date"})
lbrfig.update_yaxes(ticksuffix="%")
#employment pop ratio
emppopfig = px.line(df[df["series_id"]=="LNS12300000"], x = "date", y = "value", title = "Employment Population Ratio", labels = {"value":"Unemployment %", "date":"Date"})
emppopfig.update_yaxes(ticksuffix="%")
#manufacturing
manfig = px.line(df[df["series_id"]=="CES3000000001"], x = "date", y = "value")
#leisure and hospitality
leisfig = px.line(df[df["series_id"]=="CES7000000001"], x = "date", y = "value")
#average hourly earnings
hourfig = px.line(df[df["series_id"]=="CES0500000003"], x = "date", y = "value")


chartlist = ["Nonfarm Employment", "Employment Pop Ratio", "Unemploymetn Rate", "Manufacturing Ratio","Leisure and Hospitality", "Average Hourly Earnings"]

tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs(chartlist)

with tab1:
    st.plotly_chart(nonfarmfig)  # Nonfarm employment
with tab2:
    st.plotly_chart(unempfig) # Unemployment rate
with tab3:
    st.plotly_chart(lbrfig) # Labor force participation
with tab4:
    st.plotly_chart(emppopfig) # Employment-pop ratio
with tab5:
    st.plotly_chart(leisfig) # Leisure & Hospitality
with tab6:
    st.plotly_chart(hourfig) # Avg hourly earnings



