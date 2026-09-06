from pathlib import Path


GEOSPATIAL_EXTENSIONS = {
    ".tif",
    ".tiff",
}

BENCHMARK_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
}


def get_file_extension(file_path: str) -> str:
    """Return the file extension in lowercase."""
    return Path(file_path).suffix.lower()


def is_geospatial_format(file_path: str) -> bool:
    """Check whether the file is TIFF/GeoTIFF."""
    return get_file_extension(file_path) in GEOSPATIAL_EXTENSIONS


def is_benchmark_format(file_path: str) -> bool:
    """Check whether the file uses an approved benchmark image format."""
    return get_file_extension(file_path) in BENCHMARK_EXTENSIONS


def is_supported_format(file_path: str) -> bool:
    """
    Check whether the extension is supported by SatQuery AI.

    PNG/JPEG are only format-level candidates.
    Benchmark eligibility will be checked by validation later.
    """
    extension = get_file_extension(file_path)

    return (
        extension in GEOSPATIAL_EXTENSIONS
        or extension in BENCHMARK_EXTENSIONS
    )


def get_file_info(file_path: str) -> dict:
    """Return basic information about the input file."""

    path = Path(file_path)

    return {
        "file_name": path.name,
        "file_extension": path.suffix.lower(),
        "file_size": path.stat().st_size if path.is_file() else 0,
        "exists": path.is_file(),
        "is_geospatial": is_geospatial_format(file_path),
        "is_benchmark_format": is_benchmark_format(file_path),
        "supported_format": is_supported_format(file_path),
    }