from click.testing import CliRunner
from engn.main import main


def test_version():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "engn, version 0.1.0" in result.output
