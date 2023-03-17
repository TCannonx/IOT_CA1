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

### IAM
Create an IAM user group for which to store the IOT thing which will be createwd for the purpose of this project.

### AWS IOT Core
* Craete and register a thing on the IOT Core and add to IAM Access Group.
* This will act as the device on which to pass the data from Node-Red to the AWS platform.
* Apply the generic AWS IOT policy to the thing.
* Download endpoint credntials, certficates and private key whcih relate to the IOT thing to personal computer for later use.

##### MQTT
In the IOT Core menu, create an mqtt message broker topic to recieve data from Node-Red and input to our table.

#### Rules
* Create SQL rule to retrieve relevant data from message broker to input to table.
* Create email messaging to notify user once the device has dropped below a certain temperature

### Node-Red
* Using Node-Red's drag and drop enviornment, add a ```Pi Hat Simulator``` Out node which is then linked to a MQTT message broker node which will be used
to publish the data from the sensor to the AWS platform.
* This MQTT node will take the endpoint credential, certificate and private key files relating to the aws thing which was created previously, to link to the
AWS platform.

### DynamoDB
* Create DynamoDB table using an identifiable name.
* Set time as the primary key for the table and device number as the sort key, with device data defining the data which will be stored to the table.
* Create an AWS rule using SQL code:
```
SELECT * FROM broker
```

* Time data should be formatted in ```$timestamp``` form to be readable for the dashboard.
* This will retrieve the data from the mqtt broker and add the table to the data.

### Dashboarding
* A real-time dashboard is created using Python with the help of the streamlit library.
The data from the DynamoDB table is queried by the script using the boto3 Python library.
* The script continuously queries the table while running to access the incoming realtime data and updates accordingly.
* The data is stored in a pandas dataframe where it is then cleaned, formatted and ordered by time. the data is also filtered by previous 24 hours.
* Minimum, maximimum, average and current values are then calculated from the daataframe to be displayed by the dashboarding application.

![Alt text](https://github.com/TCannonx/IOT_CA1/blob/main/Architecture%20Diagram.png "Architecture Diagram")

