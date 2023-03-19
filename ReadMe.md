# CA1 IoT Real Time Analytics (BSHDS4) Dashboarding Application
#### Thomas Cannon
#### x19405504@student.ncirl.ie

[Video Demonstration Link](https://youtu.be/KOmfaQE1NGE)

[Git Repository Link](https://github.com/TCannonx/IOT_CA1)

This report will detail the steps taken to analyse the live data from a Pi Sensor Hat Simulator.

### Prerequisites

* Python
  * Pandas
  * Boto3
  * Streamlit
* AWS Account
* Node.js
* Email Address

### IAM
Create an IAM user group for which to store the IOT thing which will be created for the purpose of this project.

### AWS IOT Core
* Create and register a thing on the IOT Core and add to IAM Access Group.
* This will act as the device on which to pass the data from Node-Red to the AWS platform.
* Apply the generic AWS IOT policy to the thing.
* Download endpoint credntials, certficates and private key whcih relate to the IOT thing to personal computer for later use.

##### MQTT
In the IOT Core menu, create an mqtt message broker topic to recieve data from Node-Red and input to our table.

#### Rules
* Create SQL rule to retrieve relevant data from message broker to input to table.
* Create email messaging to notify user once the device has dropped below a certain temperature

#### Email Notification
![Alt text](https://github.com/TCannonx/IOT_CA1/blob/main/images/Email%20Notification.png "Email Notification")

### Node-Red
* Using Node-Red's drag and drop enviornment, add a ```Pi Hat Simulator``` Out node which is then linked to a MQTT message broker node which will be used
to publish the data from the sensor to the AWS platform.
* Configure longitude and latitude output using an inject node ran on loop to continuously update table with location data.
* A 2 second delay is added to the circuit using the join node once both the sensor and inject nodes are merged. This is to limit the amount of data
being sent to the table. 
* This MQTT node will take the endpoint credential, certificate and private key files relating to the aws thing which was created previously, to link to the
AWS platform.

#### Node-Red Environment
![Alt text](https://github.com/TCannonx/IOT_CA1/blob/main/images/Node-Red%20Screenshot.png "Node-Red Environment")

### DynamoDB
* Create DynamoDB table using an identifiable name.
* Set time as the primary key for the table and device number as the sort key, with device data defining the data which will be stored to the table.
* Create an AWS rule using SQL code:
```
SELECT * FROM broker
```

* Time data should be formatted in ```$timestamp``` form to be readable for the dashboard.
* This will retrieve the data from the mqtt broker and add the table to the data.

### Email Notification
An email notification rule was created using AWS's ```Simple Notifictaion Service``` (SNS). This service takes SQL code to analyse incoming data
and can be used to create an email notification service.   
   
In the case of this project the user is notified when the Raspberry Pi Hat Sensor Simulator's temperature value falls below 20 degrees.
The user will then be sent an email message stating ther fall and what tge current temperature is. this is computed using the following SQL code:

```
SELECT 'The temperature level for this device has just dropped below 20. Current temperature is is currently at ' + (temperature) AS message 
FROM 'device/5/data' 
WHERE temperature < 20
```

### Data Streaming Concepts
#### Data Processing Window
This analysis makes use of a ```sliding``` data processing window. The dashbaord focuses soley on data which has been generated within the last
24 hours. For this reason the data used for calculated minimum, maximum and average totals only relate to the last 24 hours of data. 
  
This is known as a sliding data processing window because, as time progresses the window changes to exclude data which was processed 
longer than 24 hours ago.

#### Data Intervals
In some cases intervals are applied to data being uploaded to a database. An interval is defined as a certain measure of time where breaks freom uploading
data to the database are added. This is to limit the amoount of data which is uploaded to the database.  
  
In this case, it is not necessary to send the values of the sensor for every second to the AWS cloud system. For this reason, a join node is added to
add a 3 second interval to the data being uploaded. The same 3 second interval is added to the queries made by the Python script to the DynamoDB table.

### Dashboarding
* A real-time dashboard is created using Python with the help of the streamlit library.  
The data from the DynamoDB table is queried by the script using the boto3 Python library.
* The script continuously queries the table while running to access the incoming realtime data and updates accordingly.
* The data is stored in a pandas dataframe where it is then cleaned, formatted and ordered by time. the data is also filtered by previous 24 hours.
* Minimum, maximimum, average and current values are then calculated from the dataframe to be displayed by the dashboarding application.

#### Example Dashboard Output
![Alt text](https://github.com/TCannonx/IOT_CA1/blob/main/images/Dashboard%20Screenshot.png "Example Dashboard Output")

#### Architecture Diagram
![Alt text](https://github.com/TCannonx/IOT_CA1/blob/main/images/Architecture%20Diagram.png "Architecture Diagram")


