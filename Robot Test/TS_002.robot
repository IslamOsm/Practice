*** Settings ***
Resource         keywords.robot
Suite Setup      Login TestRail
Suite Teardown    Log To Console    \n\rSuite Teardown started

*** Test Cases ***
Add User
    [Documentation]    Check adding user to TestRail
    Add User To TestRail
    ${users_data}    Get Users
    ${username}    Catenate    SEPARATOR=    Test    ${TIME}
    Should Contain    ${users_data}    ${username}
    ...               Users list from TR doesn't contain user ${username}
    Log To Console    \n\rUsers list from TR contains user
    [Teardown]    Run Keywords
    ...    Run Keyword If Test Passed    Teardown Actions
    ...    AND    Run Keyword If Test Failed    Log To Console    \n\rTest Failed


