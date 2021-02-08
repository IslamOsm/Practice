*** Settings ***
Variables         RobotVariables.py
Library           Subscriber.py    ${data}[sub_username]     ${data}[sub_password]    WITH NAME    Subscribe
Library           Publisher.py    ${data}[publ_username]    ${data}[publ_password]    WITH NAME    Public


Suite Teardown    Run Keywords
...               Subscribe.stop_subscriber    AND
...               Public.stop_publisher

*** Test Cases ***
Send And Get Message
    [Documentation]    The test checks whether the publisher and subscriber can
    ...                send and receive messages, respectively
    Subscribe.start_subscriber
    Public.public_message    MU-CHAMPION
    Sleep    5
    ${result}    Subscribe.return_messages
    Should Contain     ${result}     MU-CHAMPION    ${result} doesn't contain
    ...                text





