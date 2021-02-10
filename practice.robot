*** Settings ***
Resource         Robot Test/keywords.robot
Variables        Mqtt task/RobotVariables.py
Library          Mqtt task/Subscriber.py    ${datamqtt}[sub_username]     ${datamqtt}[sub_password]
Library          Mqtt task/Publisher.py    ${datamqtt}[publ_username]    ${datamqtt}[publ_password]
Library          helpful.py


Suite Teardown   Log To Console    \n\rSuite Teardown started

*** Test Cases ***
Check User
    [Documentation]
    [Tags]    testrailid=1    defects=
    Login TestRail
    ${users_data}    Get Users
    Should Contain    ${users_data}    Islam Osmanov
    ...               Users list from TR doesn't contain user Islam Osmanov
    Should Contain    ${users_data}    etm75306@zwoho.com
    ...               Users list from TR doesn't contain user Islam Osmanov

Public And Get Messages MQTT
    [Documentation]    Check whether the publisher and subscriber can
    ...                send and receive messages, respectively
    [Tags]    testrailid=2    defects=
    [Setup]    Start Subscriber
    Public Message    MU-CHAMPION
    Sleep    5
    ${result}    Return Messages
    Should Contain     ${result}     MU-CHAMPION    ${result} doesn't contain
    ...                text
    [Teardown]        Run Keywords
    ...               Stop Subscriber    AND
    ...               Stop Publisher

Prime number
    [Documentation]    Check that time is a prime number
    [Tags]    testrailid=3    defects=
    ${date}    Time Create
    ${value}    Is Prime    ${date}
    Should Be True    ${value}    The date isn't an primary number


Platform Version
    [Documentation]    Check the version of the platform
    [Tags]    testrailid=4    defects=
    ${platform}    Return Platform Name
    Should Be Equal    ${platform}    Windows    The platform isn't Windows