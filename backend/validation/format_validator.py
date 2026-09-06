from pathlib import Path


GEOSPATIAL_EXTENSIONS = {".tif", ".tiff"}
BENCHMARK_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def validate_format(file_path: str) -> dict:
    """
    Validate the input file format according to SatQuery AI requirements.

    TIFF/GeoTIFF:
        Accepted as primary geospatial inputs.

    PNG/JPEG:
        Accepted only when the input belongs to an approved
        public benchmark dataset.

    Other formats:
        Rejected.
    """

    extension = Path(file_path).suffix.lower()

    if extension in GEOSPATIAL_EXTENSIONS:
        return {
            "valid": True,
            "extension": extension,
            "format_type": "geospatial",
            "benchmark_only": False,
            "message": "TIFF/GeoTIFF format accepted."
        }

    if extension in BENCHMARK_EXTENSIONS:
        return {
            "valid": True,
            "extension": extension,
            "format_type": "benchmark_image",
            "benchmark_only": True,
            "message": "PNG/JPEG requires approved benchmark eligibility."
        }

    return {
        "valid": False,
        "extension": extension,
        "format_type": "unsupported",
        "benchmark_only": False,
        "message": "Unsupported input format."
    }