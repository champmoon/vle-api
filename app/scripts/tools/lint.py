import sys

from black import main as black
from flake8 import __main__ as flake8
from isort import main as isort
from mypy import main as mypy

from app.scripts.tools.settings import settings


def main() -> None:
    folders = settings.FOLDERS_FOR_LINTING

    print("\nFlake8:")
    flake8.main([*folders, "--exit-zero"])

    print("\nMypy:")
    mypy.main(
        script_path=None,
        stdout=sys.stdout,
        stderr=sys.stderr,
        args=[*folders],
        clean_exit=True,
    )

    print("\nIsort:")
    isort.main([*folders, "--check-only"])

    print("\nBlack:")
    black.main([*folders, "--check"], standalone_mode=False)


if __name__ == "__main__":
    main()
