from pathlib import Path
import rasterio


def validate_modality(file_path: str, declared_modality: str) -> dict:
    """
    Validate the declared modality against the raster.

    Supported modalities:
        optical
        sar
    """

    declared_modality = declared_modality.lower().strip()

    if declared_modality not in {"optical", "sar"}:
        return {
            "valid": False,
            "modality": declared_modality,
            "message": "Unsupported modality."
        }

    path = Path(file_path)

    if not path.is_file():
        return {
            "valid": False,
            "modality": declared_modality,
            "message": "Input file does not exist."
        }

    with rasterio.open(file_path) as src:
        band_count = src.count

    return {
        "valid": True,
        "modality": declared_modality,
        "band_count": band_count,
        "message": f"{declared_modality.capitalize()} modality accepted."
    }