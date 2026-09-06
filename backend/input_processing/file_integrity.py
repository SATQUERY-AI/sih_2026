from pathlib import Path


def check_file_exists(file_path: str) -> bool:
    """Check whether the input file exists."""

    return Path(file_path).is_file()


def check_file_not_empty(file_path: str) -> bool:
    """Check whether the input file exists and is not empty."""

    path = Path(file_path)

    return path.is_file() and path.stat().st_size > 0


def validate_file_integrity(file_path: str) -> dict:
    """Perform basic integrity checks on the input file."""

    exists = check_file_exists(file_path)
    not_empty = check_file_not_empty(file_path)

    return {
        "exists": exists,
        "not_empty": not_empty,
        "valid": exists and not_empty,
    }