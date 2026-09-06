from pathlib import Path


def validate_temporal(before_file: str, after_file: str) -> dict:

    before = Path(before_file)
    after = Path(after_file)

    if not before.is_file():
        return {
            "valid": False,
            "message": "Before image does not exist."
        }

    if not after.is_file():
        return {
            "valid": False,
            "message": "After image does not exist."
        }

    if before.resolve() == after.resolve():
        return {
            "valid": False,
            "message": "Before and after images must be different."
        }

    return {
        "valid": True,
        "before_file": before.name,
        "after_file": after.name,
        "message": "Bi-temporal input pair is valid."
    }