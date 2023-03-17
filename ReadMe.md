# CA1 IoT Real Time Analytics (BSHDS4) Dashboarding Application
#### Thomas Cannon
#### x19405504@student.ncirl.ie

This file will detail the steps taken to analyse the live data from a pi sensor hat simulator.

### Prerequisites

* Python
  * Pandas
  * Boto3
  * Streamlit
* AWS Account
* Node.js
* Email Address

iot core
create iam access group

Register thing on iot core related to iam access group.
apply generic iot policy to thing

download endpoint credntials, certficates and private key to personal computer for later use

mqtt
create message broker to recieve data from node red and input to table
create email messaging to notify user once the device has dropped below a certain temperature

node-red
in node-red drag and drop enviornment add pi hat simulator out which is linked to mqtt out publishing node.
create messaging broker to send real time data from the pi hat sensor to aws.
link broker the the thing which has been registered earlier using certifcates, private key and endpoint. Subscribe to an identifiable topic which the broker will send the data to.

dynamodb
create dynamodb table using an identifiable name.
set time as the primary key for the tableand device number as the sort key, with device data defining the data which will be stored to the table.
create an aws rule using SQL code:
SELECT * FROM broker
time data should be formatted in $timestamp form to be readable for the dashboard
this will retrieve the data from the mqtt broker and add the table to the data

dashboarding
a real time dashboard is created using Python with the help of the streamlit library.
The data fromm the dynamodb table is queried by the script using the boto3 Python library

the script continuously queries the table while running to access the incoming realtime data and updates accordingly

the data is stored in a pandas dataframe where it is then cleaned, formatted and ordered by time. the data is also filtered by previous 24 hours.

minimum, maximimum, average and current values are then calculated from the daataframe to be displayed by the dashboarding application.

![Alt text](https://github.com/TCannonx/IOT_CA1/blob/main/Architecture%20Diagram.png "Architecture Diagram")

