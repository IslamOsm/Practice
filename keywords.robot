*** Settings ***
Library           DateTime
Variables         MyVariables.py
Library           adding_data.py
Library           request.py
Library           Collections
Library           APIClient.py    ${data}[url]    ${data}[username]
...                               ${data}[password]

*** Keywords ***
Login TestRail
    [Documentation]    Instantinate Client class and create class variable CLIENT
    ${cl}     Make Client    ${data}[url_notAPI]    ${data}[username]
    ...                      ${data}[password]
    Set Suite Variable    ${CLIENT}    ${cl}
    Log To Console    Authentification to TestRail

Add User To TestRail
    [Documentation]    Add user with changed data and set suite variable TIME
    ${loc_time}    Time Create
    ${data}      Return Data    ${loc_time}
    Call Method    ${CLIENT}    add_user     ${data}
    Set Suite Variable    ${TIME}    ${loc_time}
    Log To Console    Add current user to the TestRail

Get Users
    [Documentation]    Get list of users
    ${response_users}    Send Get    get_users
    ${response_users_text}     Convert To String    ${response_users[0]}
    [Return]    ${response_users_text}
    Log To Console    Get list of users

Date Generation
    [Documentation]    Generate date with time for adding to the
    ...                test case description and return it
    ${cur_time}    Get Current Date    result_format=%d/%m/%Y %H:%M:%S
    Log To Console   The process of date generation
    [Return]     ${cur_time}

Get Cases
    [Documentation]    Get the list of all cases in project and return list
    [Arguments]    ${case_num}
    ${tr}    Return Trinteract
    ${res}    Call Method    ${tr}    get_cases    ${case_num}
    Log To Console    Get list of cases
    [Return]    ${res}

Teardown Actions
    [Documentation]    Call after successful ending of the tests
    Log To Console     The user was deleted
