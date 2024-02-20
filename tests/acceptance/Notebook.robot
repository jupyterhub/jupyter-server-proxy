*** Comments ***
To learn more about these .robot files, see
https://robotframework-jupyterlibrary.readthedocs.io/en/stable/.

*** Settings ***
Documentation     Server Proxies in Notebook
Library           JupyterLibrary
Suite Setup       Start Notebook Tests
Test Tags         app:notebook

*** Variables ***
${XP_NEW_MENU}   xpath://jp-toolbar[contains(@class, "jp-FileBrowser-toolbar")]//*[contains(text(), "New")]
${XP_OPEN_COMMAND}   xpath://li[@data-command = "server-proxy:open"]

*** Test Cases ***
Notebook Loads
    Capture Page Screenshot    00-smoke.png

Launch Browser Tab
    Launch With Toolbar Menu    foo
    Wait Until Keyword Succeeds    3x    0.5s    Switch Window    title:Hello World
    Location Should Contain    foo
    Wait Until Page Contains    Hello World    timeout=10s
    Close Window
    [Teardown]    Switch Window    title:Home

Launch Another Browser Tab
    Launch With Toolbar Menu    bar
    Wait Until Keyword Succeeds    3x    0.5s    Switch Window    title:Hello World
    Location Should Contain    bar
    Wait Until Page Contains    Hello World    timeout=10s
    Close Window
    [Teardown]    Switch Window    title:Home

*** Keywords ***
Start Notebook Tests
    Open Notebook
    Tag With JupyterLab Metadata
    Set Screenshot Directory    ${OUTPUT DIR}${/}notebook

Launch With Toolbar Menu
    [Arguments]    ${title}
    Mouse Over   ${XP_NEW_MENU}
    Click Element    ${XP_NEW_MENU}
    ${item} =   Set Variable   ${XP_OPEN_COMMAND}//div[text() = '${title}']
    Wait Until Element Is Visible   ${item}
    Mouse Over   ${item}
    Click Element   ${item}
