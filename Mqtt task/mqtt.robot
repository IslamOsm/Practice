*** Settings ***
Variables         RobotVariables.py
Library           Subscriber.py    ${data}[sub_username]     ${data}[sub_password]
Library           Publisher.py    ${data}[publ_username]    ${data}[publ_password]


*** Test Cases ***
Send And Get Message
    [Documentation]    Check whether the publisher and subscriber can
    ...                send and receive messages, respectively
    [Setup]    Start Subscriber
    Public Message    MU-CHAMPION
    Sleep    5
    ${result}    Return Messages
    Should Contain     ${result}     MU-CHAMPION    ${result} doesn't contain
    ...                text
    [Teardown]        Run Keywords
    ...               Stop Subscriber    AND
    ...               Stop Publisher




