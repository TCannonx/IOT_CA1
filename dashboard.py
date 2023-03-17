# Library Imports
import streamlit as st
import pandas as pd
import time
import numpy as np
import plotly.express as px
import boto3
from datetime import datetime, timedelta

def dt_convert(val):
    '''Function applied to "sample_time" column to format datetime data.'''
    return datetime.utcfromtimestamp(val / 1000).strftime('%Y-%m-%d %H:%M:%S')

# Format Streamlit Dashboard page
st.title('Pi Hat Simulator Dashboard')
placeholder = st.empty()

# Apply AWS credentials to access DynamoDB table
REGION_NAME = 'eu-west-1'
TABLE_NAME = 'wx_data'

dynamodb = boto3.resource('dynamodb', region_name=REGION_NAME)
table = dynamodb.Table(TABLE_NAME)

previous_min_temp = 0
previous_max_temp = 0
previous_average_temp = 0
previous_recent_temp = 0

previous_min_humid = 0
previous_max_humid = 0
previous_average_humid = 0
previous_recent_humid = 0

# Loop to create data stream for sensor data
run = True
while run:

    # Retrieve latest data from table
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    # If no data is present in table, inform user  
    if not data:
        with placeholder.container():
            st.markdown("### No data to be displayed")

    else:
        # Format incoming data into readable columns
        raw_data = pd.DataFrame.from_records(data)
        extracted_data = pd.concat([raw_data, raw_data['device_data'].apply(pd.Series)], axis=1)
        extracted_data = pd.concat([extracted_data, extracted_data['environment'].apply(pd.Series)], axis=1)
        extracted_data = pd.concat([extracted_data, extracted_data['coordinate_data'].apply(pd.Series)], axis=1)
        clean_data = extracted_data.drop(['device_data', 'environment', 'coordinate_data'], axis=1)

        if 'joystick' in clean_data.columns:
            clean_data = pd.concat([clean_data, clean_data['joystick'].apply(pd.Series)], axis=1)
            clean_data = clean_data.drop(['joystick', 0, 'state'], axis=1)

        clean_data['sample_time'] = pd.to_numeric(clean_data['sample_time'])
        clean_data['sample_time'] = clean_data['sample_time'].apply(dt_convert)

        clean_data = clean_data.sort_values('sample_time')
        clean_data = clean_data.fillna(method='ffill')

        # Filter data to instances which have been uploaded within the last 24 hours
        current_time = datetime.now()
        last24_hours = (current_time - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        clean_data = clean_data[(clean_data['sample_time'] > last24_hours)]

        # Calculate minimum, maximum, average and most recent values for each data type 
        average_temp = np.mean(clean_data['temperature'])
        average_humid = np.mean(clean_data['humidity'])

        max_temp = np.max(clean_data['temperature'])
        max_humid = np.max(clean_data['humidity'])

        min_temp = np.min(clean_data['temperature'])
        min_humid = np.min(clean_data['humidity'])

        recent_temp = clean_data['temperature'].to_list()[-1]
        recent_humid = clean_data['humidity'].to_list()[-1]

        recent_temp = clean_data['temperature'].to_list()[-1]
        recent_humid = clean_data['humidity'].to_list()[-1]

        current_long = clean_data['longitude'].to_list()[-1]
        current_lat = clean_data['latitude'].to_list()[-1]

        if 'key' in clean_data.columns:
            latest_key = clean_data['key'].to_list()[-1]

        else:
            latest_key = 'None'

        # Output data values to dashborard
        with placeholder.container():

            # Temperature values
            st.subheader('Temperature Data')
            temp1, temp2, temp3, temp4 = st.columns(4)
            
            temp1.metric(
                label="Minimum Temperature",
                value = round(min_temp),
                delta = round(min_temp - previous_min_temp),
            )

            temp2.metric(
                label="Maximum Temperature",
                value = round(max_temp),
                delta = round(max_temp - previous_max_temp),
            )

            temp3.metric(
                label="Average Temperature",
                value = round(average_temp),
                delta=round(average_temp - previous_average_temp),
            )

            temp4.metric(
                label="Current Temperature",
                value=round(recent_temp),
                delta=round(recent_temp - previous_recent_temp),
            )

            # Humidity values
            st.subheader('Humidity Data')
            hum1, hum2, hum3, hum4 = st.columns(4)
            
            hum1.metric(
                label="Minimum Humidity",
                value=round(min_humid),
                delta=round(min_humid - previous_min_humid),
            )

            hum2.metric(
                label="Maximum Humidity",
                value=round(max_humid),
                delta=round(max_humid - previous_max_humid),
            )

            hum3.metric(
                label="Avgerage Humidity",
                value=round(average_humid),
                delta=round(average_humid - previous_average_humid),
            )

            hum4.metric(
                label="Current Humidity",
                value=round(recent_humid),
                delta=round(recent_humid - previous_recent_humid),
            )

            # Longitude and Latitude values
            long, lat, = st.columns(2)

            long.metric(
                label="Longitude",
                value=round(current_long),
            )

            lat.metric(
                label="Latitude",
                value=round(current_lat),
            )

            # Joystick value
            st.subheader('Joystick Data')
            st.metric(
                label='Most Recent Arrow Pressed',
                value=latest_key
                    )

            # Create Line-Charts 
            st.markdown("### Temperature Chart")
            fig1 = px.line(clean_data, x="sample_time", y="temperature", title="Temperature Over Time")
            st.write(fig1)

            st.markdown("### Humidity Chart")
            fig2 = px.line(clean_data, x="sample_time", y="humidity", title="Humidity Over Time")
            st.write(fig2)

            # Set previous values on which to calculated the delta for new values
            previous_min_temp = min_temp
            previous_max_temp = max_temp
            previous_average_temp = average_temp
            previous_recent_temp = recent_temp

            previous_min_humid = min_humid
            previous_max_humid = max_humid
            previous_average_humid = average_humid
            previous_recent_humid = recent_humid

    # Set 3 second delay on data flow to save processing
    time.sleep(3)
