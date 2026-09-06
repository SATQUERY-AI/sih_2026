from .format_validator import validate_format
from .modality_validator import validate_modality
from .metadata_validator import validate_metadata
from .spatial_validator import validate_spatial
from .compatibility_validator import validate_compatibility
from .quality_validator import validate_quality


def validate_single_image(
    file_path: str,
    modality: str,
    expected_bands: int = 3
) -> dict:

    results = {
        "format": validate_format(file_path),
        "modality": validate_modality(file_path, modality),
        "metadata": validate_metadata(file_path),
        "spatial": validate_spatial(file_path),
        "compatibility": validate_compatibility(
            file_path, expected_bands
        ),
        "quality": validate_quality(file_path),
    }

    overall_valid = all(
        result["valid"] for result in results.values()
    )

    return {
        "valid": overall_valid,
        "results": results,
        "message": (
            "Single-image input validation passed."
            if overall_valid
            else "Single-image input validation failed."
        ),
    }