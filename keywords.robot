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
    [Documentation]    Instantinate Client class and create
    ...                class instance variable CLIENT
    ${cl}     Make Client    ${data}[url_notAPI]    ${data}[username]
    ...                      ${data}[password]
    Set Suite Variable    ${CLIENT}    ${cl}
    Log To Console    \n\rAuthentification to TestRail

Add User To TestRail
    [Documentation]    Add user with changed data and set suite variable TIME
    ${loc_time}    Time Create
    ${data}      Modify Return Data    ${loc_time}
    Call Method    ${CLIENT}    add_user     ${data}
    Set Suite Variable    ${TIME}    ${loc_time}
    Log To Console    \n\rUser was added to the TestRail

Get Users
    [Documentation]    Get list of users
    ${response_users}    Send Get    get_users
    ${response_users_text}     Convert To String    ${response_users[0]}
    Log To Console    \n\rGet list of users
    [Return]    ${response_users_text}

Get Cases
    [Documentation]    Get the list of all cases in project and return list
    [Arguments]    ${case_num}
    ${tr}    Return Trinteract
    ${res}    Call Method    ${tr}    get_cases    ${case_num}
    Log To Console    \n\rGet list of cases
    [Return]    ${res}

Teardown Actions
    [Documentation]    Test Teardown, called after
    ...                successful ending of the tests
    Log To Console     \n\rThe user was deleted
