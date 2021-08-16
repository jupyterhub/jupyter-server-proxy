import subprocess
import pytest
from pathlib import Path
import shutil

HERE = Path(__file__).parent
OUTPUT = HERE.parent.parent / "build/robot"


def test_robot():
    """run acceptance tests with robotframework"""
    with_robot = pytest.importorskip("JupyterLibrary")

    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)

    return_code = subprocess.call(
        [*map(str, ["robot", "--outputdir", OUTPUT, HERE])],
        cwd=str(HERE)
    )

    assert return_code == 0
