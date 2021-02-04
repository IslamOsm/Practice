*** Settings ***
Variables         RobotVariables.py
Library           Subscriber.py    ${data}[sub_username]     ${data}[sub_password]
Library           Publisher.py     ${data}[publ_username]    ${data}[publ_password]


Suite Teardown    Run Keywords
...               Publisher.stop    AND
...               Subscriber.stop

*** Test Cases ***
Send And Get Message
    [Documentation]    The test checks whether the publisher and subscriber can
    ...                send and receive messages, respectively
    Public Message    MU-CHAMPION
    Sleep    5
    ${result}    Return Messages
    Should Contain     ${result}     MU-CHAMPION    ${result} doesn't contain
    ...                text





