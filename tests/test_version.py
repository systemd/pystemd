from pathlib import Path

import toml
from cstq import Query


def test_version():
    """all version should be the same"""
    root = Path(__file__).parent.parent
    pyproject = root / "pyproject.toml"
    setup = root / "setup.py"
    version = root / "pystemd/__version__.py"

    setup_version = (
        # pyrefly: ignore [missing-attribute]
        Query(setup)
        .find_function_call(func_name="setup")
        .extended_node()
        .keyword_args["version"]
        .literal_eval()
    )
    version_version = (
        Query(version).find_assignment("__version__").value.literal_eval_for_node()
    )
    pyproject_version = toml.loads(pyproject.read_text())["project"]["version"]
    assert setup_version == version_version == pyproject_version
