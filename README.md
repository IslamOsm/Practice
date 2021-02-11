# Robot Test

Python 3.9

Robot Framework 3.2.2

Internal Libraries:

-- DateTime

-- Process

TS_002.robot

Check process of adding user to TestRail

To run the code: ```robot TS_002.robot```


# Python TestRail tests

Python 3.7

request.py 
Adds the user to TestRail

tests_request.py
Performs tests for the request.py

congig.ini
Parameters of user

To run the program launch the following program of adding the user
```
python request.py
```
To run the tests 
```
pytest tests_request.py
```

# Linux Task

Python 3.8

Ubuntu 20.04.1 LTS

# Add Data to TestRail

adding_data.py

Add date to the description of the project in TestRail

To run code

```
python adding_data.py
```

tests_adding_data.py

Test of adding data code

To run the code

```
pytest tests_adding_data.py
```


# MQTT PRACTICE

Python 3.9

Robot Framework 3.2.2

Broker: "test.mosquitto.org" 

Using topic: "mqtttest/TC_002"

mqtt_task.py

Execution of interaction between subscriber and publisher through a broker

To run the code:  ```python mqtt_task.py```


mqtt.robot

Check whether subscribers can accept messages from a publisher

To run the code: ```robot mqtt.robot```

# PRACTICE

Python 3.7

Robot Framework 3.2.2

To execute practice.robot suite with reporting to TestRail

```robot --listener src/TestRailListener.py:testuser123i.testrail.io:etm75306@zwoho.com:7aetO03XW6tVycV00UPk:1:https:update practice.robot```

Report is sent to TestRail run_id=1 in example below 