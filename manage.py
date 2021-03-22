import os, sys
from src.commands import cli

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath("./tools"))
    cli()
else:
    from src.app import create_app
    app = create_app()
