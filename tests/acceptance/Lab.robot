*** Comments ***
To learn more about these .robot files, see
https://robotframework-jupyterlibrary.readthedocs.io/en/stable/.

*** Settings ***
Documentation     Server Proxies in Lab
Library           JupyterLibrary
Suite Setup       Start Lab Tests
Test Tags         app:lab


*** Test Cases ***
Lab Loads
    Capture Page Screenshot    00-smoke.png

*** Keywords ***
Start Lab Tests
    Open JupyterLab
    Tag With JupyterLab Metadata
    Set Screenshot Directory    ${OUTPUT DIR}${/}lab
