import rasterio


def extract_metadata(file_path: str) -> dict:
    """
    Extract metadata required for SatQuery AI
    GeoTIFF/TIFF processing and validation.
    """

    with rasterio.open(file_path) as src:
        metadata = {
            "file_name": src.name.split("\\")[-1].split("/")[-1],
            "width": src.width,
            "height": src.height,
            "band_count": src.count,
            "dtype": src.dtypes[0],
            "crs": str(src.crs) if src.crs else None,
            "driver": src.driver,
            "transform": str(src.transform),
            "bounds": {
                "left": src.bounds.left,
                "bottom": src.bounds.bottom,
                "right": src.bounds.right,
                "top": src.bounds.top,
            },
            "resolution": {
                "x": src.res[0],
                "y": src.res[1],
            },
        }

    return metadata