*** Settings ***
Library           DateTime
Library           adding_data.py
Library           req.py
Library           Collections
Library           APIClient.py    https://osmisl.testrail.io/    hzr11101@cuoly.com    .hUsjsGJDnid..VCRLV6

*** Keywords ***
Time Generation
    [Documentation]   Generate unix time for user's add data
    ${loc_time}    Time Generation
    ${TIME}    Set Variable    ${loc_time}
    Log To Console    The process of time generation
    Set Global Variable    ${TIME}

Login TestRail
    [Documentation]    Instantinates Client class
    Time Generation
    ${cl}     Make Client    https://osmisl.testrail.io/index.php?/    hzr11101@cuoly.com    .hUsjsGJDnid..VCRLV6
    ${CLIENT}    Set Variable    ${cl}
    Log To Console    Authentification to TestRail
    Set Global Variable    ${CLIENT}

Add User To TestRail
    [Documentation]    Add user with changed data
    ${data}      Return Data    ${TIME}
    Call Method    ${CLIENT}    add_user     ${data}
    Log To Console    Adding current user to the TestRail

Get Users
    [Documentation]    Gets list of users
    ${response_users}    Send Get    get_users
    ${RESPONSE_USERS_TEXT}     Convert To String    ${response_users[0]}
    [Return]    ${RESPONSE_USERS_TEXT}
    Log To Console    Get list of users

Date Generation
    [Documentation]    Generates date with time for adding to the
    ...                test case description
    ${cur_time}    Get Current Date    result_format=%d/%m/%Y %H:%M:%S
    Log To Console   The process of date generation
    [Return]     ${cur_time}

Get Cases
    [Documentation]    Gets thre list of all cases in project
    [Arguments]    ${case_num}
    ${tr}    Return Trinteract
    ${res}    Call Method    ${tr}    get_cases    ${case_num}
    Log To Console    Get list of cases
    [Return]    ${res}

Teardown Actions
    [Documentation]    Called after successful ending of the tests
    Log To Console    The user was deleted

Fail Test
    Log to console    The user was not added