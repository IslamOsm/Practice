*** Settings ***
Library           mqtt_task.py

*** Keywords ***
Create Publisher
    [Documentation]    Create Publisher and variable for publishing messages
    ${PUBLISHER}    Generate Publisher
    Set Suite Variable    ${PUBLISHER}
    log to console    Creating publisher

Create Subscriber
    [Documentation]    Create Subscriber and variable to subscribe to the topic
    ${SUBSCRIBER}     Generate Subscriber
    Set Suite Variable    ${SUBSCRIBER}
    log to console    Creating subscriber
