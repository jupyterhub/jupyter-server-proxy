*** Comments ***
To learn more about these .robot files, see
https://robotframework-jupyterlibrary.readthedocs.io/en/stable/.

*** Settings ***
Documentation     Server Proxies in Lab
Library           JupyterLibrary
Suite Setup       Start Lab Tests
Test Tags         app:lab


*** Variables ***
${CSS_LAUNCHER_CARD}   css:.jp-LauncherCard-label

*** Test Cases ***
Lab Loads
    Capture Page Screenshot    00-smoke.png

Custom Category Icon
    ${selector} =    Set Variable    css:.jp-LauncherCard[title^="foo"] .jp-LauncherCard-icon > *
    Wait Until Element Is Visible    ${selector}    timeout=10s
    ${item} =    Get WebElement    ${selector}
    ${background_image} =    Execute Javascript
    ...    return window.getComputedStyle(arguments[0]).backgroundImage;
    ...    ARGUMENTS    ${item}
    Should Contain    ${background_image}    /server-proxy/icon/foo

Launch Browser Tab
    Click Launcher    foo
    Wait Until Keyword Succeeds    3x    0.5s    Switch Window    title:Hello World
    Location Should Contain    foo
    Wait Until Page Contains    Hello World    timeout=10s
    Close Window
    [Teardown]    Switch Window    title:JupyterLab

Launch Lab Tab
    Click Launcher    bar
    Wait Until Page Contains Element    css:iframe
    Select Frame    css:iframe
    Wait Until Page Contains    Hello World    timeout=10s

*** Keywords ***
Start Lab Tests
    Open JupyterLab
    Tag With JupyterLab Metadata
    Set Screenshot Directory    ${OUTPUT DIR}${/}lab

Click Launcher
    [Arguments]    ${title}
    ${item} =   Set Variable   ${CSS_LAUNCHER_CARD}\[title^\="${title}"]
    Wait Until Element Is Visible  ${item}  timeout=10s
    Click Element    ${item}
