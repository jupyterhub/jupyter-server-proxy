*** Comments ***
To learn more about these .robot files, see
https://robotframework-jupyterlibrary.readthedocs.io/en/stable/.

*** Settings ***
Documentation     Server Proxies in Lab
Library           JupyterLibrary
Suite Setup       Start Lab Tests

*** Test Cases ***
Lab Loads
    Capture Page Screenshot    00-smoke.png

Launch Browser Tab
    Click Launcher    foo
    Wait Until Keyword Succeeds    3x    0.5s    Switch Window    title:Hello World
    Location Should Contain    foo
    Page Should Contain    Hello World
    Close Window
    [Teardown]    Switch Window    title:JupyterLab

Launch Lab Tab
    Click Launcher    bar
    Wait Until Page Contains Element    css:iframe
    Select Frame    css:iframe
    Page Should Contain    Hello World

*** Keywords ***
Start Lab Tests
    Open JupyterLab
    Tag With JupyterLab Metadata
    Set Screenshot Directory    ${OUTPUT DIR}${/}lab

Click Launcher
    [Arguments]    ${title}
    Click Element    css:.jp-LauncherCard-label[title^\="${title}"]
