*** Settings ***
Library           adding_data.py
Library           Process
Resource          keywords.robot

Suite Setup     Login TestRail

*** Variables ***
${REQ_URL_USERS}    get_users
${REQ_URL_CASES}    get_cases/1

*** Test Cases ***
Test Added User
    [Documentation]       Check availability to get users info
    Add User To TestRail
    ${users_data}    Get Users
    ${username}    Catenate    SEPARATOR=    Test    ${TIME}
    Should Contain    ${users_data}    ${username}


Test Added Data
    [Documentation]       Check process of adding date
    ${time}    Date Generation
    main TRInteract    ${time}
    ${response}    Get Cases    case_num=1
    ${response_text}    convert to string    ${response}
    Should Contain    ${response_text}    ${time}

Get Cases Status Code
    [Documentation]    Checks correctness of method's status code
    ${time}    Date Generation
    ${status_code}    main TRInteract    ${time}
    Should Be Equal As Integers    ${status_code}    200

Get Cases With Wrong Data
    [Documentation]    Checks the inability of getting info
    ...                with wrong data
    ${err_msg}    Run Keyword And Return Status    Get Cases    case_num=234
    ${err_text}    Convert To String    ${err_msg}
    Should Be Equal    ${err_text}    False

Get Cases Data Size
    [Documentation]    Checks list of users
    ${response_users}    Send Get    ${REQ_URL_USERS}
    ${response_size}    Get Length    ${RESPONSE_USERS}
    Should Not Be Equal    ${response_size}    0


