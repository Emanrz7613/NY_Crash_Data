import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import matplotlib.pyplot as plt
import numpy as np


@st.cache_data
def load_data(data_file):
    df = pd.read_csv(data_file)
    return df

data_file = 'data2.csv'
df = load_data(data_file)

st.markdown("<img src='https://miro.medium.com/v2/resize:fit:800/0*qME_9ndLowgvyYPZ.jpeg' alt='I Love NY' width='700'/>", unsafe_allow_html=True)


st.markdown("# New York City Crash Data")
st.markdown("## The Most Dangerous Places in NYC for Pedestrians, Cyclists, and Motorists")
st.markdown("### Where is Someone More Likely to get Injured or Killed in Each Borough")


def load_geojson(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Load the local GeoJSON data
geojson_path = 'nyc_boroughs.geojson'  
nyc_boroughs_geojson = load_geojson(geojson_path)

st.title("New York City Boroughs Map")

# Dropdown to select a borough
selected_borough = st.selectbox("Select a Borough to View", ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"])
selected_borough_upper = selected_borough.upper()

# Function to calculate the totals for the selected borough
def calculate_totals_for_borough(df, borough_name):
    borough_data = df[df['boro_name'] == borough_name]
    total_killed = borough_data['NUMBER OF PERSONS KILLED'].sum()
    total_injured = borough_data['NUMBER OF PERSONS INJURED'].sum()
    return total_killed, total_injured

# Function to highlight the selected borough and calculate totals
def highlight_borough(geojson, borough_name, df):
    highlight_color = [180, 0, 200, 140]  # Highlight color
    default_color = [200, 200, 200, 80]   # Default color

    # Call calculate_totals_for_borough here to ensure fresh calculation on each selection
    selected_borough_total_killed, selected_borough_total_injured = calculate_totals_for_borough(df, selected_borough_upper)

    # Convert totals to int to ensure JSON serializability
    total_killed = int(selected_borough_total_killed)
    total_injured = int(selected_borough_total_injured)

    for feature in geojson['features']:
        feature['properties']['color'] = default_color
        if feature['properties']['boro_name'] == borough_name:
            feature['properties']['color'] = highlight_color
            # Assign the totals to each feature's properties
            feature['properties']['total_killed'] = total_killed
            feature['properties']['total_injured'] = total_injured
        
    return geojson

# Update GeoJSON based on the selected borough and get totals for tooltip
highlighted_geojson = highlight_borough(nyc_boroughs_geojson, selected_borough, df)


# Pydeck map
view_state = pdk.ViewState(latitude=40.7128, longitude=-74.0060, zoom=9)
layer = pdk.Layer(
    type='GeoJsonLayer',
    data=highlighted_geojson,
    get_fill_color='properties.color',
    pickable=True    
)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=True))

# Create tabs for different categories
tab1, tab2, tab3 = st.tabs(["Pedestrians", "Cyclists", "Motorists"])

with tab1:
    st.title(f"Pedestrian Data for {selected_borough}")

    filtered_df = df[df['boro_name'] == selected_borough_upper]


        # Extract relevant columns from your DataFrame
    pedestrians_df = filtered_df[['ON STREET NAME', 'NUMBER OF PEDESTRIANS KILLED', 'NUMBER OF PEDESTRIANS INJURED']]

    # Group the data by 'ON STREET NAME' and calculate the sum of pedestrians killed and injured
    pedestrians_sum_df = pedestrians_df.groupby('ON STREET NAME').agg({
        'NUMBER OF PEDESTRIANS KILLED': 'sum',
        'NUMBER OF PEDESTRIANS INJURED': 'sum'
    }).reset_index() 
    


    # Sort the data by the sum of pedestrians injured and killed in descending order
    pedestrians_injured_df = pedestrians_sum_df.sort_values(by='NUMBER OF PEDESTRIANS INJURED', ascending=False).head(5)
    pedestrians_killed_df = pedestrians_sum_df.sort_values(by='NUMBER OF PEDESTRIANS KILLED', ascending=False).head(5)

    # Get the top street name
    top_street_name_injured = pedestrians_injured_df.iloc[0]['ON STREET NAME'].title()
    top_street_name_killed = pedestrians_killed_df.iloc[0]['ON STREET NAME'].title()

    # Create a bar chart for top 5 streets with the highest number of pedestrians injured
    st.header(f"Pedestrians Are More Likely to get Injured on {top_street_name_injured}")
    fig, ax1 = plt.subplots()

    # Set the x-axis positions for the bars
    x1 = np.arange(len(pedestrians_injured_df))

    # Create the bars for pedestrians injured (blue color)
    bars_injured = ax1.bar(x1, pedestrians_injured_df['NUMBER OF PEDESTRIANS INJURED'], label='Injured', color='blue')

    ax1.set_xlabel('Street Name')
    ax1.set_ylabel('Count')
    ax1.set_title('Pedestrians Injured By Street Name (Top 5)')
    ax1.set_xticks(x1)
    ax1.set_xticklabels(pedestrians_injured_df['ON STREET NAME'])
    ax1.legend()

    # Annotate the bars with their values (as integers)
    for bar in bars_injured:
        height = bar.get_height()
        ax1.annotate(f'{height}',  # Convert to integers
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset for better alignment
                    textcoords="offset points",
                    ha='center', va='bottom')

    # Set the y-axis ticks to show integer values starting from 0
    plt.yticks(range(0, int(pedestrians_injured_df['NUMBER OF PEDESTRIANS INJURED'].max()) + 1))

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Create a bar chart for top 5 streets with the highest number of pedestrians killed
    st.header(f"Pedestrians Are More Likely to get Killed on {top_street_name_killed}")
    fig, ax2 = plt.subplots()

    # Set the x-axis positions for the bars
    x2 = np.arange(len(pedestrians_killed_df))

    # Create the bars for pedestrians killed (red color)
    bars_killed = ax2.bar(x2, pedestrians_killed_df['NUMBER OF PEDESTRIANS KILLED'], label='Killed', color='red')

    ax2.set_xlabel('On-Street Name')
    ax2.set_ylabel('Count')
    ax2.set_title('Pedestrians Killed by Street Name (Top 5)')
    ax2.set_xticks(x2)
    ax2.set_xticklabels(pedestrians_killed_df['ON STREET NAME'])
    ax2.legend()

    # Annotate the bars with their values (as integers)
    for bar in bars_killed:
        height = bar.get_height()
        ax2.annotate(f'{int(height)}',  # Convert to integers
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset for better alignment
                    textcoords="offset points",
                    ha='center', va='bottom')

    # Set the y-axis ticks to show integer values starting from 0
    plt.yticks(range(0, int(pedestrians_killed_df['NUMBER OF PEDESTRIANS KILLED'].max()) + 1))

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    st.pyplot(fig)

        # Extract the time of day from the "CRASH TIME" column and convert it to datetime
    filtered_df['CRASH TIME'] = pd.to_datetime(filtered_df['CRASH TIME'])

    # Define time intervals for quarters
    morning_start = pd.to_datetime('05:00:00').time()
    late_morning_start = pd.to_datetime('09:00:00').time()
    afternoon_start = pd.to_datetime('13:00:00').time()
    evening_start = pd.to_datetime('19:00:00').time()

    # Categorize the time into quarters
    def categorize_time(time):
        if morning_start <= time < late_morning_start:
            return 'Morning (5:00 AM - 9:00 AM)'
        elif late_morning_start <= time < afternoon_start:
            return 'Late Morning (9:00 AM - 1:00 PM)'
        elif afternoon_start <= time < evening_start:
            return 'Afternoon (1:00 PM - 7:00 PM)'
        else:
            return 'Evening (7:00 PM onwards)'

    # Apply the categorization to create a new column "Time Quarter"
    filtered_df['Time Quarter'] = filtered_df['CRASH TIME'].apply(lambda x: categorize_time(x.time()))

    # Calculate the sum of people injured and killed in each quarter
    quarterly_summary = filtered_df.groupby('Time Quarter')[['NUMBER OF PEDESTRIANS INJURED', 'NUMBER OF PEDESTRIANS KILLED']].sum()

    # Create a pie chart to visualize the data
    st.title("What Time of Day is the Safest and Most Dangerous for Motorist Injuries and Fatalities")
    fig, ax = plt.subplots()

    # Create a list of labels including both percentage and numerical sum
    labels = [f'{quarter}\n{quarterly_summary["NUMBER OF PEDESTRIANS INJURED"][quarter]:.0f} Injured, {quarterly_summary["NUMBER OF PEDESTRIANS KILLED"][quarter]:.0f} Killed\n({quarterly_summary["NUMBER OF PEDESTRIANS INJURED"][quarter] + quarterly_summary["NUMBER OF PEDESTRIANS KILLED"][quarter]:.0f} Total)' for quarter in quarterly_summary.index]

    ax.pie(quarterly_summary.sum(axis=1), labels=labels, startangle=90, autopct='%1.1f%%', pctdistance=0.85)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Show the pie chart in Streamlit
    st.pyplot(fig)


with tab2:
    st.title(f"Cyclist Data for {selected_borough}")

    filtered_df = df[df['boro_name'] == selected_borough_upper]


        # Extract relevant columns from your DataFrame
    cyclist_df = filtered_df[['ON STREET NAME', 'NUMBER OF CYCLIST KILLED', 'NUMBER OF CYCLIST INJURED']]

    # Group the data by 'ON STREET NAME' and calculate the sum of cyclist killed and injured
    cyclist_sum_df = cyclist_df.groupby('ON STREET NAME').agg({
        'NUMBER OF CYCLIST KILLED': 'sum',
        'NUMBER OF CYCLIST INJURED': 'sum'
    }).reset_index()   



    # Sort the data by the sum of cyclist injured and killed in descending order
    cyclist_injured_df = cyclist_sum_df.sort_values(by='NUMBER OF CYCLIST INJURED', ascending=False).head(5)
    cyclist_killed_df = cyclist_sum_df.sort_values(by='NUMBER OF CYCLIST KILLED', ascending=False).head(5)

    # Get the top street name
    top_street_name_injured = cyclist_injured_df.iloc[0]['ON STREET NAME'].title()
    top_street_name_killed = cyclist_killed_df.iloc[0]['ON STREET NAME'].title()

    # Create a bar chart for top 5 streets with the highest number of cyclist injured
    st.header(f"Cyclist Are More Likely to get Injured on {top_street_name_injured}")
    fig, ax1 = plt.subplots()

    # Set the x-axis positions for the bars
    x1 = np.arange(len(cyclist_injured_df))

    # Create the bars for cyclist injured (blue color)
    bars_injured = ax1.bar(x1, cyclist_injured_df['NUMBER OF CYCLIST INJURED'], label='Injured', color='blue')

    ax1.set_xlabel('Street Name')
    ax1.set_ylabel('Count')
    ax1.set_title('cyclist Injured By Street Name (Top 5)')
    ax1.set_xticks(x1)
    ax1.set_xticklabels(cyclist_injured_df['ON STREET NAME'])
    ax1.legend()

    # Annotate the bars with their values (as integers)
    for bar in bars_injured:
        height = bar.get_height()
        ax1.annotate(f'{height}',  # Convert to integers
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset for better alignment
                    textcoords="offset points",
                    ha='center', va='bottom')

    # Set the y-axis ticks to show integer values starting from 0
    plt.yticks(range(0, int(cyclist_injured_df['NUMBER OF CYCLIST INJURED'].max()) + 1))

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Create a bar chart for top 5 streets with the highest number of Cyclists killed
    st.header(f"Cyclists Are More Likely to get Killed on {top_street_name_killed}")
    fig, ax2 = plt.subplots()

    # Set the x-axis positions for the bars
    x2 = np.arange(len(cyclist_killed_df))

    # Create the bars for Cyclists killed (red color)
    bars_killed = ax2.bar(x2, cyclist_killed_df['NUMBER OF CYCLIST KILLED'], label='Killed', color='red')

    ax2.set_xlabel('On-Street Name')
    ax2.set_ylabel('Count')
    ax2.set_title('Cyclists Killed by Street Name (Top 5)')
    ax2.set_xticks(x2)
    ax2.set_xticklabels(cyclist_killed_df['ON STREET NAME'])
    ax2.legend()

    # Annotate the bars with their values (as integers)
    for bar in bars_killed:
        height = bar.get_height()
        ax2.annotate(f'{int(height)}',  # Convert to integers
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset for better alignment
                    textcoords="offset points",
                    ha='center', va='bottom')

    # Set the y-axis ticks to show integer values starting from 0
    plt.yticks(range(0, int(cyclist_killed_df['NUMBER OF CYCLIST KILLED'].max()) + 1))

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    st.pyplot(fig)

        # Extract the time of day from the "CRASH TIME" column and convert it to datetime
    filtered_df['CRASH TIME'] = pd.to_datetime(filtered_df['CRASH TIME'])

    # Define time intervals for quarters
    morning_start = pd.to_datetime('05:00:00').time()
    late_morning_start = pd.to_datetime('09:00:00').time()
    afternoon_start = pd.to_datetime('13:00:00').time()
    evening_start = pd.to_datetime('19:00:00').time()

    # Categorize the time into quarters
    def categorize_time(time):
        if morning_start <= time < late_morning_start:
            return 'Morning (5:00 AM - 9:00 AM)'
        elif late_morning_start <= time < afternoon_start:
            return 'Late Morning (9:00 AM - 1:00 PM)'
        elif afternoon_start <= time < evening_start:
            return 'Afternoon (1:00 PM - 7:00 PM)'
        else:
            return 'Evening (7:00 PM onwards)'

    # Apply the categorization to create a new column "Time Quarter"
    filtered_df['Time Quarter'] = filtered_df['CRASH TIME'].apply(lambda x: categorize_time(x.time()))

    # Calculate the sum of Cyclists injured and killed in each quarter
    quarterly_summary = filtered_df.groupby('Time Quarter')[['NUMBER OF CYCLIST INJURED', 'NUMBER OF CYCLIST KILLED']].sum()

    # Create a pie chart to visualize the data
    st.title("What Time of Day is the Safest and Most Dangerous for Cyclist Injuries and Fatalities")
    fig, ax = plt.subplots()

    # Create a list of labels including both percentage and numerical sum
    labels = [f'{quarter}\n{quarterly_summary["NUMBER OF CYCLIST INJURED"][quarter]:.0f} Injured, {quarterly_summary["NUMBER OF CYCLIST KILLED"][quarter]:.0f} Killed\n({quarterly_summary["NUMBER OF CYCLIST INJURED"][quarter] + quarterly_summary["NUMBER OF CYCLIST KILLED"][quarter]:.0f} Total)' for quarter in quarterly_summary.index]

    ax.pie(quarterly_summary.sum(axis=1), labels=labels, startangle=90, autopct='%1.1f%%', pctdistance=0.85)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Show the pie chart in Streamlit
    st.pyplot(fig)

with tab3:
    st.title(f"Motorist Data for {selected_borough}")

    filtered_df = df[df['boro_name'] == selected_borough_upper]


        # Extract relevant columns from your DataFrame
    motorist_df = filtered_df[['ON STREET NAME', 'NUMBER OF MOTORIST KILLED', 'NUMBER OF MOTORIST INJURED']]

    # Group the data by 'ON STREET NAME' and calculate the sum of motorist killed and injured
    motorist_sum_df = motorist_df.groupby('ON STREET NAME').agg({
        'NUMBER OF MOTORIST KILLED': 'sum',
        'NUMBER OF MOTORIST INJURED': 'sum'
    }).reset_index()   



    # Sort the data by the sum of motorist injured and killed in descending order
    motorist_injured_df = motorist_sum_df.sort_values(by='NUMBER OF MOTORIST INJURED', ascending=False).head(5)
    motorist_killed_df = motorist_sum_df.sort_values(by='NUMBER OF MOTORIST KILLED', ascending=False).head(5)

    # Get the top street name
    top_street_name_injured = motorist_injured_df.iloc[0]['ON STREET NAME'].title()
    top_street_name_killed = motorist_killed_df.iloc[0]['ON STREET NAME'].title()

    # Create a bar chart for top 5 streets with the highest number of motorist injured
    st.header(f"Motorist Are More Likely to get Injured on {top_street_name_injured}")
    fig, ax1 = plt.subplots()

    # Set the x-axis positions for the bars
    x1 = np.arange(len(motorist_injured_df))

    # Create the bars for motorist injured (blue color)
    bars_injured = ax1.bar(x1, motorist_injured_df['NUMBER OF MOTORIST INJURED'], label='Injured', color='blue')

    ax1.set_xlabel('Street Name')
    ax1.set_ylabel('Count')
    ax1.set_title('Motorist Injured By Street Name (Top 5)')
    ax1.set_xticks(x1)
    ax1.set_xticklabels(motorist_injured_df['ON STREET NAME'])
    ax1.legend()

    # Annotate the bars with their values (as integers)
    for bar in bars_injured:
        height = bar.get_height()
        ax1.annotate(f'{height}',  # Convert to integers
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset for better alignment
                    textcoords="offset points",
                    ha='center', va='bottom')

    # # Set the y-axis ticks to show integer values starting from 0
    # plt.yticks(range(0, int(motorist_injured_df['NUMBER OF MOTORIST INJURED'].max()) + 1))

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Create a bar chart for top 5 streets with the highest number of motorist killed
    st.header(f"Motorist Are More Likely to get Killed on {top_street_name_killed}")
    fig, ax2 = plt.subplots()

    # Set the x-axis positions for the bars
    x2 = np.arange(len(motorist_killed_df))

    # Create the bars for Cyclists killed (red color)
    bars_killed = ax2.bar(x2, motorist_killed_df['NUMBER OF MOTORIST KILLED'], label='Killed', color='red')

    ax2.set_xlabel('Street Name')
    ax2.set_ylabel('Count')
    ax2.set_title('Motorist Killed by Street Name (Top 5)')
    ax2.set_xticks(x2)
    ax2.set_xticklabels(motorist_killed_df['ON STREET NAME'])
    ax2.legend()

    # Annotate the bars with their values (as integers)
    for bar in bars_killed:
        height = bar.get_height()
        ax2.annotate(f'{int(height)}',  # Convert to integers
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset for better alignment
                    textcoords="offset points",
                    ha='center', va='bottom')

    # Set the y-axis ticks to show integer values starting from 0
    plt.yticks(range(0, int(motorist_killed_df['NUMBER OF MOTORIST KILLED'].max()) + 1))

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    st.pyplot(fig)

        # Extract the time of day from the "CRASH TIME" column and convert it to datetime
    filtered_df['CRASH TIME'] = pd.to_datetime(filtered_df['CRASH TIME'])

    # Define time intervals for quarters
    morning_start = pd.to_datetime('05:00:00').time()
    late_morning_start = pd.to_datetime('09:00:00').time()
    afternoon_start = pd.to_datetime('13:00:00').time()
    evening_start = pd.to_datetime('19:00:00').time()

    # Categorize the time into quarters
    def categorize_time(time):
        if morning_start <= time < late_morning_start:
            return 'Morning (5:00 AM - 9:00 AM)'
        elif late_morning_start <= time < afternoon_start:
            return 'Late Morning (9:00 AM - 1:00 PM)'
        elif afternoon_start <= time < evening_start:
            return 'Afternoon (1:00 PM - 7:00 PM)'
        else:
            return 'Evening (7:00 PM onwards)'

    # Apply the categorization to create a new column "Time Quarter"
    filtered_df['Time Quarter'] = filtered_df['CRASH TIME'].apply(lambda x: categorize_time(x.time()))

    # Calculate the sum of motorist injured and killed in each quarter
    quarterly_summary = filtered_df.groupby('Time Quarter')[['NUMBER OF MOTORIST INJURED', 'NUMBER OF MOTORIST KILLED']].sum()

    # Create a pie chart to visualize the data
    st.title("What Time of Day is the Safest and Most Dangerous for Motorist Injuries and Fatalities")
    fig, ax = plt.subplots()

    # Create a list of labels including both percentage and numerical sum
    labels = [f'{quarter}\n{quarterly_summary["NUMBER OF MOTORIST INJURED"][quarter]:.0f} Injured, {quarterly_summary["NUMBER OF MOTORIST KILLED"][quarter]:.0f} Killed\n({quarterly_summary["NUMBER OF MOTORIST INJURED"][quarter] + quarterly_summary["NUMBER OF MOTORIST KILLED"][quarter]:.0f} Total)' for quarter in quarterly_summary.index]

    ax.pie(quarterly_summary.sum(axis=1), labels=labels, startangle=90, autopct='%1.1f%%', pctdistance=0.85)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Show the pie chart in Streamlit
    st.pyplot(fig)








