*** Settings ***
Documentation     Acceptance tests for jupyter-server-proxy
Library           JupyterLibrary
Library           OperatingSystem
Suite Setup       Set Up
Suite Teardown    Clean Up

*** Keywords ***
Set Up
    ${notebook dir} =    Set Variable    ${OUTPUT DIR}${/}notebooks
    Copy Directory    resources    ${notebook dir}
    Wait For New Jupyter Server To Be Ready
    ...    stdout=${OUTPUT DIR}${/}server.log
    ...    notebook_dir=${notebook dir}
    ...    cwd=${notebook dir}

Clean Up
    Close all Browsers
    Terminate All Jupyter Servers
