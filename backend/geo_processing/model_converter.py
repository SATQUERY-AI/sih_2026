import numpy as np
from .raster_reader import read_raster
from .normalization import normalize_raster


def generate_model_ready_representation(file_path: str) -> dict:
    """
    Generate a model-ready representation from a GeoTIFF/TIFF.

    The original raster file is not modified.
    """

    raster_data, profile = read_raster(file_path)

    normalized_data = normalize_raster(raster_data)

    return {
        "data": normalized_data,
        "shape": normalized_data.shape,
        "dtype": str(normalized_data.dtype),
        "min_value": float(normalized_data.min()),
        "max_value": float(normalized_data.max()),
        "band_count": normalized_data.shape[0],
        "height": normalized_data.shape[1],
        "width": normalized_data.shape[2],
        "crs": str(profile["crs"]) if profile.get("crs") else None,
    }