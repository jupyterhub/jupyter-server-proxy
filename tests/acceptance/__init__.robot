*** Comments ***
To learn more about these .robot files, see
https://robotframework-jupyterlibrary.readthedocs.io/en/stable/.

*** Settings ***
Documentation     Acceptance tests for jupyter-server-proxy
Library           JupyterLibrary
Library           OperatingSystem
Library           Process
Suite Setup       Set Up
Suite Teardown    Clean Up

*** Keywords ***
Set Up
    ${notebook dir} =    Set Variable    ${OUTPUT DIR}${/}notebooks
    Copy Directory    resources    ${notebook dir}
    Set Screenshot Directory   EMBED
    Set Environment Variable
    ...    name=JUPYTER_CONFIG_DIR
    ...    value=${notebook dir}
    Wait For New Jupyter Server To Be Ready
    ...    %{JUPYTER_LIBRARY_APP_COMMAND}
    ...    stdout=${OUTPUT DIR}${/}server.log
    ...    notebook_dir=${notebook dir}
    ...    cwd=${notebook dir}

Clean Up
    Close all Browsers
    Terminate All Jupyter Servers
    Terminate All Processes
