*** Settings ***
Library           APIClient.APIClient    https://islamosm.testrail.io/    gch47858@cuoly.com    tSlFeh0QWe1bM8WfJsXU
Library           DateTime
Library           TRInteract.TRInteract
Library           Process
*** Variables ***
${REQ_URL_USERS}    get_users
${REQ_URL_CASES}    get_cases/1

*** Keywords ***
Run wrong cases
    ${RESPONSE}=    Get Cases    234

*** Test Cases ***
Test added user
    [Documentation]       The test case checks availability to get users info
    ${RESPONSE_USERS}=    Send Get    ${REQ_URL_USERS}
    ${RESPONSE_USERS_TEXT}=     Convert To String    ${RESPONSE_USERS[0]}
    Should Contain    ${RESPONSE_USERS_TEXT}    Islam Osmanov
    Should Contain    ${RESPONSE_USERS_TEXT}    gch47858@cuoly.com


Test added_data
    [Documentation]       The test case checks process of adding date
    Run Process    python    TRInteract.py
    ${RESPONSE_CASES}=    Send Get    ${REQ_URL_CASES}
    ${RESPONSE_CASES_TEXT}=     Convert To String    ${RESPONSE_CASES[0]}
    ${CUR_TIME}=    Get Current Date    result_format=%d/%m/%Y
    ${CUR_TIME_TEXT}=    Convert To String    ${CUR_TIME}

    Should Contain    ${RESPONSE_CASES_TEXT}    ${CUR_TIME_TEXT}

Get cases status code
    [Documentation]    The test case check correctness of method's status code
    Get Cases    1
    ${lib}=    Get Library Instance    TRInteract.TRInteract
    Should Be Equal As Integers    ${lib.status_code}    200

Get cases with wrong data
    [Documentation]    The test case checks the inability of getting info
    ...                with wrong data
    ${ERR_MSG}=    Run Keyword And Return Status    Run wrong cases
    ${ERR_TEXT}=    Convert To String    ${ERR_MSG}
    Should Be Equal    ${ERR_TEXT}    False

Get cases data size
    [Documentation]    The test case checks list of users
    ${RESPONSE_USERS}=    Send Get    ${REQ_URL_USERS}
    ${RESPONSE_SIZE}=    Get Length    ${RESPONSE_USERS}
    Should Not Be Equal    ${RESPONSE_SIZE}    0

Post description
    [Documentation]    The test case checks availability of adding date
    Get Cases    1
    Change Description
    ${RESULT}=    post description
    ${RESULT_TEXT}=    Convert To String    ${RESULT[0][1]}
    Should Be Equal     ${RESULT_TEXT}    200

Dates in cases
    [Documentation]    The test cases check list of users with their
    ...                information, after adding data in prediction
    Get Cases    1
    Change Description
    ${DATES}=    Check Date
    FOR    ${DATE}    IN    ${DATES[0]}
        ${DATE_TEXT}=    Convert To String    ${DATE}
        Should Be Equal    ${DATE_TEXT}  True
    END