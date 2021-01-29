*** Settings ***
Library           mqtt_task.py
Resource          mqtt_keywords.robot

Suite Setup       Run Keywords
...               Create Publisher    AND
...               Create Subscriber


*** Test Cases ***
Send And Get Message
    [Documentation]    The test checks whether the publisher and subscriber can
    ...                send and receive messages, respectively
    Send Message    MU-Champion    ${PUBLISHER}
    Get Message    ${SUBSCRIBER}
    ${result}    Return List Messages    ${SUBSCRIBER}
    Should Contain     ${result}     MU-Champion
    [Teardown]  Stop      ${PUBLISHER}





