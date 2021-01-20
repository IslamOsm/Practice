*** Settings ***
Library           APIClient.py    https://islamosm.testrail.io/    gch47858@cuoly.com    tSlFeh0QWe1bM8WfJsXU
Library           DateTime
Library           TRInteract.py
Library           Process
*** Variables ***
${REQ_URL_USERS}    get_users
${REQ_URL_CASES}    get_cases/1

*** Keywords ***
Run wrong cases
    ${RESPONSE}=    Get Cases    234

*** Test Cases ***
# Test added user
#     [Documentation]       Check ability to get users from TestRail
#     ${users}    API Get Users
#     ${users_text}    Convert To String    ${users[0]}
#     Should Contain    ${users_text}    Islam Osmanov
#     Should Contain    ${users_text}    gch47858@cuoly.com


Test Adding Data
    [Documentation]    Check process of adding date
    Get Cases    project_id=1
    ${timestamp}    Change Description
    ${check_date}    Check Date
    Run Keyword If    ${check_date} != @{EMPTY}    Post Description

    ${cases}    API Get Cases    project_id=1
    
    FOR  ${case}  IN  ${cases}
        ${case_text}    Convert To String    ${case}
        Should Contain    ${case_text}    ${timestamp}
    END

Get cases status code
    [Documentation]    The test case check correctness of method's status code
    Get Cases    1
    ${lib}=    Get Library Instance    TRInteract
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