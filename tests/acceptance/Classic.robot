*** Comments ***
To learn more about these .robot files, see
https://robotframework-jupyterlibrary.readthedocs.io/en/stable/.

*** Settings ***
Documentation     Server Proxies in Notebook Classic
Library           JupyterLibrary
Suite Setup       Start Notebook Classic Tests
Test Setup        Switch Window    MAIN
Test Tags         app:classic

*** Keywords ***
Start Notebook Classic Tests
    Open Notebook Classic
    Set Screenshot Directory    ${OUTPUT DIR}${/}notebook-classic

Click Launcher
    [Arguments]    ${title}
    Click Element    css:#new-dropdown-button
    Click Element    css:a[role\="menuitem"][href*="${title}"]

*** Test Cases ***
Notebook Classic Loads
    Capture Page Screenshot    00-smoke.png

Launch Browser Tab
    Click Launcher    foo
    Wait Until Keyword Succeeds    3x    0.5s    Switch Window    title:Hello World
    Location Should Contain    foo
    Wait Until Page Contains    Hello World    timeout=10s
    Close Window

Launch Another Browser Tab
    Click Launcher    bar
    Wait Until Keyword Succeeds    3x    0.5s    Switch Window    title:Hello World
    Location Should Contain    bar
    Wait Until Page Contains    Hello World    timeout=10s
    Close Window
