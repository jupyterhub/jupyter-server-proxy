import os
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE.parent.parent / "build/robot"


def test_robot():
    """run acceptance tests with robotframework"""
    robot_args = [
        "robot",
        "--consolecolors=on",
        "--include=app:lab",
        "--exitonfailure",
        f"--outputdir={OUTPUT}",
    ]

    env = dict(**os.environ)
    env.update(
        JUPYTER_LIBRARY_APP_COMMAND="jupyter-server",
        JUPYTER_LIBRARY_APP="ServerApp",
    )

    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)

    return_code = subprocess.call(
        [*robot_args, str(HERE)],
        cwd=str(HERE),
        env=env,
    )

    assert return_code == 0
