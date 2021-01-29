*** Settings ***
Library           adding_data.py
Library           Process
Resource          keywords.robot

Suite Setup     Login TestRail

*** Test Cases ***
Test Added User
    [Documentation]       Check availability to get users info
    Add User To TestRail
    ${users_data}    Get Users
    ${username}    Catenate    SEPARATOR=    Test    ${TIME}
    Should Contain    ${users_data}    ${username}
    [Teardown]    Run Keyword If Test Failed   log to console    Failed to add user

Test Added Data
    [Documentation]       Check process of adding date
    ${date}    Date Generation
    main TRInteract    ${date}
    ${response}    Get Cases    case_num=1
    ${response_text}    convert to string    ${response}
    Should Contain    ${response_text}    ${date}
    [Teardown]    Run Keyword If Test Failed   log to console    Time was not found

Get Cases Status Code
    [Documentation]    Check correctness of method's status code
    ${date}    Date Generation
    ${status_code}    main TRInteract    ${date}
    Should Be Equal As Integers    ${status_code}    200
    [Teardown]    Run Keyword If Test Failed   log to console    Status code doesn't equal 200

Get Cases With Wrong Data
    [Documentation]    Check the inability of getting info
    ...                with wrong data
    ${err_msg}    Run Keyword And Return Status    Get Cases    case_num=234
    ${err_text}    Convert To String    ${err_msg}
    Should Be Equal    ${err_text}    False
    [Teardown]    Run Keyword If Test Failed   log to console    This test case exists


Get Cases Data Size
    [Documentation]    Check list of users
    ${response_users}    Send Get     get_users
    ${response_size}    Get Length    ${response_users}
    Should Not Be Equal    ${response_size}    0
    [Teardown]    Run Keyword If Test Failed   log to console    Number of users equals 0


