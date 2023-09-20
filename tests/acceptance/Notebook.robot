*** Comments ***
To learn more about these .robot files, see
https://robotframework-jupyterlibrary.readthedocs.io/en/stable/.

*** Settings ***
Documentation     Server Proxies in Notebook
Library           JupyterLibrary
Suite Setup       Start Notebook Tests
Test Tags         app:notebook

*** Test Cases ***
Notebook Loads
    Capture Page Screenshot    00-smoke.png

*** Keywords ***
Start Notebook Tests
    Open Notebook
    Tag With JupyterLab Metadata
    Set Screenshot Directory    ${OUTPUT DIR}${/}notebook

Click Launcher
    [Arguments]    ${title}
    Click Element    css:.jp-LauncherCard-label[title^\="${title}"]
