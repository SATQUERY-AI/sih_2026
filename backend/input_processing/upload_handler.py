from pathlib import Path
import shutil

from .file_reader import get_file_info
from .file_integrity import validate_file_integrity


def save_uploaded_file(
    source_path: str,
    destination_dir: str,
) -> dict:
    """
    Validate and save an input file.

    Format eligibility is checked here at a basic level.
    Detailed benchmark, modality, spatial and temporal
    validation belongs to the validation stage.
    """

    integrity = validate_file_integrity(source_path)

    if not integrity["valid"]:
        raise ValueError("Input file does not exist or is empty.")

    file_info = get_file_info(source_path)

    if not file_info["supported_format"]:
        raise ValueError(
            f"Unsupported input format: "
            f"{file_info['file_extension']}"
        )

    destination = Path(destination_dir)
    destination.mkdir(parents=True, exist_ok=True)

    output_path = destination / file_info["file_name"]

    shutil.copy2(source_path, output_path)

    return {
        "success": True,
        "file_name": file_info["file_name"],
        "file_path": str(output_path),
        "file_extension": file_info["file_extension"],
        "file_size": output_path.stat().st_size,
    }