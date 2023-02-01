import subprocess

from black import main as black
from isort import main as isort

from app.scripts.tools.settings import settings


def main() -> None:
    folders = settings.FOLDERS_FOR_FORMATTING

    isort.main([*folders, "--force-single-line-imports"])
    subprocess.run(
        [
            "autoflake",
            "--remove-all-unused-imports",
            "--recursive",
            "--remove-unused-variables",
            "--in-place",
            *folders,
            "--exclude=__init__.py",
        ]
    )
    isort.main([*folders])
    black.main([*folders])


if __name__ == "__main__":
    main()
