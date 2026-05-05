import streamlit as st
import requests
import json
import time
import datetime
import pandas as pd
import plotly.express as px

df = pd.read_csv("masterdata.csv")





print(df)
st.set_page_config(
    page_title="BLS Labor Dashboard",
    layout="wide"
)
st.title("U.S. Labor Statistics")
st.caption("Labor Statistics by Month from Bureau of Labor Statistics")
#how do i add labels and stuff?

#nonfarm empoyment
#ok so these will be like main stuff becuase, its important and stuff. 
nonfarmfig = px.line(df[df["series_id"]=="CES0000000001"], x = "date", y = "value", title = "Nonfarm Employment", labels = {"value":"", "date": "Date"})
#unemployment rate, y axis is unemployment rate
unempfig = px.line(df[df["series_id"]=="LNS14000000"], x = "date", y = "value", title = "Unemployment Rate", labels = {"value": "Unemployment %", "date": "Date"}, template = "plotly_dark" )
unempfig.update_yaxes(range=[0,100],ticksuffix="%")

#what does this stuff mean
# labor force participation
pop_df = df[df["series_id"].isin([
    "LNS11300000",
    "LNS12300000"
])].copy() 
pop_df["Population"] = pop_df["series_id"].map({
    "LNS11300000": "US Citizen Population",
    "LNS12300000": "Total US Population"
})
lbrfig = px.line(pop_df, x = "date", y = "value", colors = "Population", title = "Labor Force Statistics", labels= {"value": "Percentage of Population Employed %", "date": "Date"})
lbrfig.update_yaxes(ticksuffix="%")
#employment pop ratio
#emppopfig = px.line(df[df["series_id"]=="LNS12300000"], x = "date", y = "value", title = "Employment Population Ratio", labels = {"value":"Percentage of Total Population Employed %", "date":"Date"})
#emppopfig.update_yaxes(ticksuffix="%")


#manufacturing leisure comparison graph
sector_df = df[df["series_id"].isin([
    "CES3000000001",
    "CES7000000001"
])].copy() 
sector_df["sector"] = sector_df["series_id"].map({
    "CES3000000001": "Manufacturing",
    "CES7000000001": "Leisure and Hospitality"
})
manfig = px.line(sector_df, x = "date", y = "value", color = 'sector', title = "Manufacturing vs Leisure Workers", labels = {"value":"Total Number of Workers", "date":"Date"})
#leisure and hospitality
#leisfig = px.line(df[df["series_id"]=="CES7000000001"], x = "date", y = "value", title = "")
#average hourly earnings    
#hourfig = px.line(df[df["series_id"]=="CES0500000003"], x = "date", y = "value")


#chartlist = ["Nonfarm Employment", "Employment Pop Ratio", "Unemploymetn Rate", "Manufacturing Ratio","Leisure and Hospitality", "Average Hourly Earnings"]

#tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs(chartlist)
unempser = df[df["series_id"]=="LNS14000000"].sort_values("date")
nonfarmseries = df[df["series_id"]== "CES0000000001"].sort_values("date")
print(unempser["value"].iloc[-1])

#with tab1:
#what kind of markers at the top?
st.metric(label = "Unemployment Rate", value = f"{unempser["value"].iloc[-1]}%")
#this is the most recent number from how many employees or whatever, laborers, all labor is forced labor? just kidding work is fun 
numberuh = nonfarmseries["value"].iloc[-1]
            
st.metric(label = "Total Non Farm Workers", value = f"{numberuh:,.0f}")
st.plotly_chart(nonfarmfig)  
#with tab2:
st.plotly_chart(unempfig) 
#with tab3:
st.plotly_chart(lbrfig) 
#with tab4:
st.plotly_chart(emppopfig) 
#with tab5:
st.plotly_chart(manfig) # Leisure and the manuacturing
#with tab6:
#st.plotly_chart(hourfig) # Avg hourly earnings



