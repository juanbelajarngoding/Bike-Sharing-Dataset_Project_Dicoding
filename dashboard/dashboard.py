import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# Title Page
st.set_page_config(page_title="Bike Sharing Dataset")

# Fungsi Label di plot bar
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

# Read file csv
day_df = pd.read_csv('day_clean.csv')
hour_df = pd.read_csv('hour_clean.csv')

# Process Data
day_df.sort_values(by="datetime", inplace=True)
hour_df.sort_values(by="datetime", inplace=True)
day_df['datetime'] = pd.to_datetime(day_df['datetime'])
hour_df['datetime'] = pd.to_datetime(hour_df['datetime'])

# Function to summmary the total of user category
def cnt_user(df):
    casual = df['casual'].sum()
    registered = df['registered'].sum()
    count = df['count'].sum()
    return casual,registered,count

# Function to make BarPlot
def make_bar_Plot(df_x,df_y,labelx=None,labely=None,labelrotation=0):
    figx, ax = plt.subplots(figsize=(6, 6))
    ax.bar(df_x, df_y, color='#FBA000')
    ax.tick_params(axis='x', labelsize=10,rotation=labelrotation)
    ax.set_ylabel(labely)
    ax.set_xlabel(labelx)
    addlabels(df_x,df_y)
    st.pyplot(figx)

# Function to make LinePlot
def make_Line_Plot(df_x,df_y,labelx=None,labely=None,labelrotation=0, color="#FBA000"):
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(df_x,df_y, color="#FBA000")
    ax.set_ylabel(labely)
    ax.set_xlabel(labelx)
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10,rotation=labelrotation)
    st.pyplot(fig)

# Making Sidebar 
min_date = hour_df["datetime"].min()
max_date = hour_df["datetime"].max()
with st.sidebar:
    st.image("bike.jpg")

    # Making data filter
    start_date, end_date = st.date_input(
        label='Date filter',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Process data according to the date range entered
main_day_df = day_df[(day_df["datetime"] >= str(start_date)) & (day_df["datetime"] <= str(end_date))]
main_hour_df = hour_df[(hour_df["datetime"] >= str(start_date)) & (hour_df["datetime"] <= str(end_date))]

# Dashboard Header
st.header('Bike Sharing Dataset:bike:')
st.write("This Dashboard was created to fullfill to meet the criteria needed to pass Dicoding: Belajar Analisis Data dengan Python")

st.markdown("""
### About Me
- *Name*: Juan Samuel Christopher
- *Email*: juansamuelchris@gmail.com
- *Dicoding ID*: juansamuel
            
### Project Overview
This dashboard will gives you the result of my analysis of bike sharing data.
""")

# Overview Data
st.subheader('The Overview Data of Rides :fire:')
casual,registered,count = cnt_user(main_day_df)
col1, col2, col3 = st.columns(3)

with col1:
        st.write("Casual User")
        st.subheader(casual)
with col2:
        st.write("Registered User")
        st.subheader(registered)    
with col3:
        st.write("Count")
        st.subheader(count)
make_Line_Plot(main_day_df['datetime'],main_day_df['count'],None,None,45, color="#FBA000") 


# Filter days in a week bike rents
st.subheader('Days in the week rentals')
# Group by weekday and aggregate statistics
weekly_stats_df = main_day_df.groupby('weekday').agg({
    'count': ['max', 'min', 'mean', 'sum', 'std']
})
# Group by weekday and sum the count
weekly_rents_df = main_day_df.groupby('weekday')['count'].sum().reset_index()
# Plotting
st.subheader("Number of Bicycle Rentals per Day of the Week")
plt.figure(figsize=(10, 5))
sns.barplot(data=weekly_rents_df, x="weekday", y="count", color="orange", errorbar=None)
plt.xlabel('Days in a week')
plt.ylabel('Total rentals')
plt.xticks(ticks=[0, 1, 2, 3, 4, 5, 6], labels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
st.pyplot(plt)


# Filter data for the year 2011
st.subheader('Bicycle usage trends have changed over the years')
monthly_2011_df = day_df[day_df['year'] == 0][['month', 'count']].groupby('month').sum()
monthly_2011_df = monthly_2011_df.reset_index()
# showing rent data on 2011
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_2011_df["month"], monthly_2011_df["count"], marker='o', linewidth=2, color="#FBA000")
ax.set_title("Distribution of Bicycle Rentals per Month in (2011)", fontsize=20)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fontsize=10)
ax.set_yticklabels(ax.get_yticks(), fontsize=10)
st.pyplot(fig)

# Filter data for the year 2012
monthly_2012_df = day_df[day_df['year'] == 1][['month', 'count']].groupby('month').sum()
monthly_2012_df = monthly_2012_df.reset_index()
# showing rent data on 2011
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_2012_df["month"], monthly_2012_df["count"], marker='o', linewidth=2, color="#FBA000")
ax.set_title("Distribution of Bicycle Rentals per Month in (2012)", fontsize=20)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fontsize=10)
ax.set_yticklabels(ax.get_yticks(), fontsize=10)
st.pyplot(fig)

st.write("Based on the provided data, it is evident that there has been a substantial increase in bike usage over the specified time periods. In both years mentioned (2011 and 2012), there is a clear trend of rising bike rentals from January onwards, reaching a peak in June for 2011 and September for the current year. However, following the peak months, there is a notable decline in bike rentals, with usage decreasing steadily towards the end of each year. This suggests a seasonal pattern in bike usage, with warmer months typically seeing higher demand. Furthermore, in 2012 appears to exhibit even higher levels of bike rentals compared to the previous year, indicating a potential increase in the popularity and adoption of biking as a mode of transportation")


# Making rent graph based on season
st.markdown("""---""")
st.header('Seasonly Rents')

season_rental = main_day_df[['count','season']].groupby(by='season').sum().reset_index()
season_map = {1: 'springer', 2: 'summer', 3: 'fall', 4: 'winter'}
season_rental['season'] = season_rental['season'].map(season_map)
season_rental.sort_values(by='count',inplace=True)
season_rental = season_rental.reset_index()
col1, col2, col3 = st.columns([1,4,1])
with col2:
    make_bar_Plot(season_rental["season"],season_rental["count"],None,'count',45)
st.write("Based on the provided data, it's evident that the count of bike rentals varies significantly across different seasons. Fall, represented by index 2, has the highest count of bike rentals at 1,061,129, followed closely by Summer with 918,589 rentals. Winter comes next with 841,613 retanls, while spring has the lowest count at 471,348 rentals. This suggests a seasonal pattern in bike rental demand, with colder seasons like winter and fall seeing higher demand compared to warmer seasons like summer and spring. This trend is likely influenced by weather conditions, with milder temperatures and more favorable biking conditions attracting higher rental numbers during warmer months. Overall, understanding these seasonal variations can be crucial for planning and managing bike rental services effectively to meet the fluctuating demands throughout the year.")

# Calculate correlation matrix
correMtr = main_hour_df[["temp", "atemp", "hum", "windspeed", "count"]].corr()
mask = np.array(correMtr)
mask[np.tril_indices_from(mask)] = False

# Plot correlation matrix
st.subheader('Correlation matrix of attributes')
fig, ax = plt.subplots(figsize=(20, 5))
sns.heatmap(correMtr, mask=mask, vmax=0.8, square=True, annot=True, ax=ax)
ax.set_title('Correlation matrix of attributes')
st.pyplot(plt)

# Scatter plot between count rental and temperature
st.subheader('Scatter plot: Count Rental vs Temperature')
plt.figure(figsize=(8, 6))
plt.scatter(x=main_day_df['count'], y=main_day_df['temp'])
plt.xlabel('Count Rental')
plt.ylabel('Temperature')
st.pyplot(plt)