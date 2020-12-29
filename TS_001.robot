*** Settings ***
Library           testrail.APIClient    https://testrequests.testrail.io/    tap02557@cuoly.com    8ZMBfZ67fERlgHVOfeId
Library           DateTime
Library           adding_data.TRInteract
Library           testrail.APIError
Library           Process
*** Variables ***
${REQ_URL_USERS}    get_users
${REQ_URL_CASES}    get_cases/1

*** Keywords ***
Run wrong cases
    ${response}=    get cases    2

*** Test Cases ***
Test added user
    ${response_users}=    send get    ${REQ_URL_USERS}
    ${response_users_text}=     convert to string    ${response_users[0]}
    should contain    ${response_users_text}    Michail
    should contain    ${response_users_text}    michail23@gmail.com


Test added_data
    run process    python    adding_data.py
    ${response_cases}=    send get    ${REQ_URL_CASES}
    ${response_cases_text}=     convert to string    ${response_cases[0]}
    ${cur_time}=    get current date    result_format=%d/%m/%Y
    ${cur_time_text}=    convert to string    ${cur_time}

    should contain    ${response_cases_text}    ${cur_time_text}

Test get cases status code
    ${response}=    get cases    1
    ${lib}=    get library instance    adding_data.TRInteract
    should be equal as integers    ${lib.status_code}    200

Test get cases with wrong data
    ${err_msg}=    Run Keyword And Ignore Error    APIError   Run wrong cases
    should be equal    ${err_msg[0]}    FAIL

Test get cases data size
    ${response_users}=    send get    ${REQ_URL_USERS}
    ${response_size}=    get length    ${response_users}
    should not be equal    ${response_size}    0

Test post description
    ${get}=    get cases    1
    change description
    should not be empty    post description

Test dates in cases
    get cases    1
    change description
    ${dates}=    check date
    log to console    ${dates}
    FOR    ${date}    IN    ${dates[0]}
        ${bool_text}=    convert to string    ${date}
        log to console    ${date}
        should be equal    ${bool_text}  True
    END