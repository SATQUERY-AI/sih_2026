from pathlib import Path
import rasterio


def validate_compatibility(file_path: str, expected_bands: int = 3) -> dict:
    path = Path(file_path)

    if not path.is_file():
        return {
            "valid": False,
            "message": "Input file does not exist."
        }

    try:
        with rasterio.open(file_path) as src:
            band_count = src.count
            width = src.width
            height = src.height

            bands_valid = band_count == expected_bands
            dimensions_valid = width > 0 and height > 0

            valid = bands_valid and dimensions_valid

            return {
                "valid": valid,
                "band_count": band_count,
                "width": width,
                "height": height,
                "checks": {
                    "bands": bands_valid,
                    "dimensions": dimensions_valid
                },
                "message": (
                    "Input is compatible with the expected configuration."
                    if valid
                    else "Input is not compatible with the expected configuration."
                )
            }

    except Exception as e:
        return {
            "valid": False,
            "message": f"Unable to validate input compatibility: {str(e)}"
        }