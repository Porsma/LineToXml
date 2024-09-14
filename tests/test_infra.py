import os.path


def test_infra():
    mandatory_files = (
        ".flake8",
        ".gitignore",
        "README.md",
        "requirements.txt"
    )

    for file in mandatory_files:
        assert os.path.isfile(file)
