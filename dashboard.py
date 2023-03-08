import streamlit as st
import pandas as pd
import random
import time
import numpy as np
import plotly.express as px
import boto3
from datetime import datetime

def dt_convert(val):
    return datetime.utcfromtimestamp(val / 1000).strftime('%Y-%m-%d %H:%M:%S')

st.title('test app')

placeholder = st.empty()

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

run = True
while run:

    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
        
    if not data:
        with placeholder.container():
            st.markdown("### No data to be displayed")

    else:
        raw_data = pd.DataFrame.from_records(data)
        clean_data = pd.concat([raw_data, raw_data["device_data"].apply(pd.Series)], axis=1)
        clean_data = clean_data.drop(['device_data'], axis=1)

        clean_data['sample_time'] = pd.to_numeric(clean_data['sample_time'])
        clean_data['sample_time'] = clean_data['sample_time'].apply(dt_convert)

        clean_data = clean_data.sort_values('sample_time')

        clean_data = clean_data.fillna(method='ffill')
        clean_data.fillna('None')

        average_temp = np.mean(clean_data['temperature'])
        average_humid = np.mean(clean_data['humidity'])

        max_temp = np.max(clean_data['temperature'])
        max_humid = np.max(clean_data['humidity'])

        min_temp = np.min(clean_data['temperature'])
        min_humid = np.min(clean_data['humidity'])

        recent_temp = clean_data['temperature'].to_list()[-1]
        recent_humid = clean_data['humidity'].to_list()[-1]

        if 'key' in clean_data.columns:
            latest_key = clean_data['key'].to_list()[-1]

        else:
            latest_key = 'None'

        with placeholder.container():

            st.subheader('Temperature Data')

            # create three columns
            temp1, temp2, temp3, temp4 = st.columns(4)

            # fill in those three columns with respective metrics or KPIs
            temp1.metric(
                label="Min Temp ⏳",
                value = round(min_temp),
                delta = round(min_temp - previous_min_temp),
            )

            temp2.metric(
                label="Max temp ⏳",
                value = round(max_temp),
                delta = round(max_temp - previous_max_temp),
            )

            temp3.metric(
                label="Avg Temp ⏳",
                value = round(average_temp),
                delta=round(average_temp - previous_average_temp),
            )

            temp4.metric(
                label="Current Temp ⏳",
                value=round(recent_temp),
                delta=round(recent_temp - previous_recent_temp),
            )

            st.subheader('Humidity Data')

            hum1, hum2, hum3, hum4 = st.columns(4)

            # fill in those three columns with respective metrics or KPIs
            hum1.metric(
                label="Min Humid ⏳",
                value=round(min_humid),
                delta=round(min_humid - previous_min_humid),
            )

            hum2.metric(
                label="Max Humid ⏳",
                value=round(max_humid),
                delta=round(max_humid - previous_max_humid),
            )

            hum3.metric(
                label="Avg Humid ⏳",
                value=round(average_humid),
                delta=round(average_humid - previous_average_humid),
            )

            hum4.metric(
                label="Current Humid ⏳",
                value=round(recent_humid),
                delta=round(recent_humid - previous_recent_humid),
            )

            st.subheader('Joystick Data')

            st.metric(
                label='Most Recent Arrow Pressed',
                value=latest_key
                    )

                            
            st.markdown("### First Chart")
            fig1 = px.line(clean_data, x="sample_time", y="temperature", title="Temperature Over Time")
            st.write(fig1)


            st.markdown("### Second Chart")
            fig2 = px.line(clean_data, x="sample_time", y="humidity", title="Humidity Over Time")
            st.write(fig2)

            previous_min_temp = min_temp
            previous_max_temp = max_temp
            previous_average_temp = average_temp
            previous_recent_temp = recent_temp

            previous_min_humid = min_humid
            previous_max_humid = max_humid
            previous_average_humid = average_humid
            previous_recent_humid = recent_humid


    # st.dataframe(database)
    time.sleep(1)

