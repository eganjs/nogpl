from pathlib import Path
from textwrap import dedent

import pytest
from click.testing import CliRunner

from nogpl.cli import cli


@pytest.fixture
def runner():
    cli_runner = CliRunner()
    with cli_runner.isolated_filesystem():
        yield cli_runner


def test_report_all_no_poetry_lock_file(runner):
    result = runner.invoke(cli, ["report", "all"])

    assert result.output == dedent(
        """\
        Usage: cli report all [OPTIONS]
        Try 'cli report all --help' for help.

        Error: Invalid value for '-f' / '--lock-file': Could not open file: poetry.lock: No such file or directory
        """
    )
    assert result.exit_code == 2


def test_report_all_empty_poetry_lock_file(runner):
    Path("poetry.lock").touch()

    result = runner.invoke(cli, ["report", "all"])

    assert result.output == ""
    assert result.exit_code == 0


def test_report_single_dependency(runner):
    Path("poetry.lock").write_text(
        dedent(
            """\
            [[package]]
            category = "main"
            description = "Composable command line interface toolkit"
            name = "click"
            optional = false
            python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*"
            version = "7.1.2"
            """
        )
    )

    result = runner.invoke(cli, ["report", "all"])

    assert result.output == dedent(
        """\
        click 7.1.2 BSD-3-Clause
        """
    )
    assert result.exit_code == 0
