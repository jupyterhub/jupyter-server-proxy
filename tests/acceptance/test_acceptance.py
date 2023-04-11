import os
import shutil
import subprocess
from pathlib import Path

import pytest

HERE = Path(__file__).parent
OUTPUT = HERE.parent.parent / "build/robot"
JUPYTER_SERVER_INFO = None

try:
    import jupyter_server

    JUPYTER_SERVER_INFO = jupyter_server.version_info
except ImportError:
    pass


def test_robot():
    """run acceptance tests with robotframework"""
    pytest.importorskip("JupyterLibrary")

    env = dict(**os.environ)

    # JUPYTER_LIBRARY_* env vars documentation:
    # https://robotframework-jupyterlibrary.readthedocs.io/en/stable/LIMITS.html#notebookapp-vs-serverapp
    if JUPYTER_SERVER_INFO is None:
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
        env=env,
    )

    assert return_code == 0
