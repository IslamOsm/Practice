*** Settings ***
Library           DateTime
Library           adding_data.py
Library           req.py
Library           Collections
Library           APIClient.py    https://osmisl.testrail.io/    hzr11101@cuoly.com    .hUsjsGJDnid..VCRLV6
Library           Datetime
*** Variables ***
${REQ_URL_USERS}    get_users
${REQ_URL_CASES}    get_cases/1

*** Keywords ***
Time Generation
    [Documentation]   Keyword generate unix time for user's add data
    ${loc_time}    Time Gen
    ${TIME}    Set Variable    ${loc_time}
    Set Global Variable    ${TIME}

Login TestRail
    [Documentation]    Keyword instantinates Client class
    Time Generation
    ${cl}=     Make Client    https://osmisl.testrail.io/index.php?/    hzr11101@cuoly.com    .hUsjsGJDnid..VCRLV6
    ${CLIENT}    Set Variable    ${cl}
    Set Global Variable    ${CLIENT}

Add User To TestRail
    [Documentation]    The keyword add user with changed data
    ${data}=      Ret Data    ${TIME}
    Call Method    ${CLIENT}    add_user     ${data}

Get Users
    [Documentation]    The keyword gets list of users
    ${response_users}=    Send Get    ${REQ_URL_USERS}
    ${RESPONSE_USERS_TEXT}=     Convert To String    ${response_users[0]}
    Return From Keyword    ${RESPONSE_USERS_TEXT}

Date Generation
    [Documentation]    The keywords generates date with time for adding to the
    ...                test case description
    ${cur_time}=    Get Current Date    result_format=%d/%m/%Y %H:%M:%S
    ${cur_time_text}=    Convert To String    ${cur_time}
    Return From Keyword     ${cur_time_text}

Get Cases
    [Documentation]    The keywords gets thre list of all cases in project
    [Arguments]    ${case_num}
    ${tr}    Ret Trint
    ${res}=    Call Method    ${tr}    get_cases    ${case_num}
    Return From Keyword    ${res}

Teardown Actions
    [Documentation]    Keyword is called after successful ending of the tests
    Log To Console    The user was deleted
