from pathlib import Path
import os
import shutil
import subprocess

import pytest

HERE = Path(__file__).parent
OUTPUT = HERE.parent.parent / "build/robot"
SERVER_INFO = None
LAB_INFO = None

try:
    import jupyter_server
    SERVER_INFO = jupyter_server.version_info
except ImportError:
    pass


def test_robot():
    """run acceptance tests with robotframework"""
    with_robot = pytest.importorskip("JupyterLibrary")

    env = dict(**os.environ)

    if SERVER_INFO is None:
        env.update(
            JUPYTER_LIBRARY_APP_COMMAND="jupyter-notebook",
            JUPYTER_LIBRARY_APP="NotebookApp",
        )
    else:
        env.update(
            JUPYTER_LIBRARY_APP_COMMAND="jupyter-server",
            JUPYTER_LIBRARY_APP="ServerApp",
        )


    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)

    return_code = subprocess.call(
        ["robot", "--consolecolors=on", f"--outputdir={OUTPUT}", str(HERE)],
        cwd=str(HERE),
        env=env
    )

    assert return_code == 0
