*** Settings ***
Resource         keywords.robot
Suite Setup      Login TestRail

*** Test Cases ***
Add User
    [Documentation]    Check adding user in TestRail
    Add User To TestRail
    ${users_data}    Get Users
    ${username}    Catenate    SEPARATOR=    Test    ${TIME}
    Should Contain    ${users_data}    ${username}
    [Teardown]    run keyword if test failed    Fail Test
    [Teardown]    Run Keyword If Test Passed    Teardown Actions


