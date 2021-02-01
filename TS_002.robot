*** Settings ***
Resource         keywords.robot
Suite Setup      Login TestRail

*** Test Cases ***
Add User
    [Documentation]    Check adding user in TestRail
    Add User To TestRail
    ${users_data}    Get Users
    ${username}    Catenate    SEPARATOR=    Test    ${TIME}
    Should Not Contain    ${users_data}    ${username}
    ...               Users list from TR doesn't contain user ${username}
    [Teardown]    Run Keywords
    ...    Run Keyword If Test Passed    Teardown Actions
    ...    AND    Run Keyword If Test Failed    Log To Console    Test Failed


