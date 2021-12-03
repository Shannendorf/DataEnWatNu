import pytest

from src.commands import drop_db, generate_testdata


@pytest.fixture
def cli(app):
    cli_runner = app.test_cli_runner()
    cli_runner.test_db = app.test_db
    return cli_runner


class TestDropDB:
    def test_drop_db(self, cli):
        # GIVEN a cli runner
        # WHEN we run the drop-db command
        # THEN the drop-db command is run
        result = cli.invoke(drop_db)
        assert result.exit_code == 0

    def test_with_alembic_table(self, cli):
        # GIVEN a cli runner and a database with a alembic table
        # WHEN we run the drop-db command
        # THEN the drop-db command is run
        conn = cli.test_db.engine.raw_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS alembic_version (id INTEGER PRIMARY KEY AUTOINCREMENT);")
        conn.commit()
        cursor.close()
        result = cli.invoke(drop_db)
        assert result.exit_code == 0
        assert not cli.test_db.engine.has_table("alembic_version")

    
class TestGenerateTestdata:
    def test_generate_testdata(self, cli):
        # GIVEN a cli runner
        # WHEN we run the generate_testdata command
        # THEN test data is generated
        result = cli.invoke(generate_testdata)
        assert result.exit_code == 0
