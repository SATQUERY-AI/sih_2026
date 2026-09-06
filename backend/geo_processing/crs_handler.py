import rasterio


def get_crs(file_path: str) -> dict:
    """
    Extract and validate the CRS of a raster.
    """

    with rasterio.open(file_path) as src:
        crs = src.crs

        return {
            "crs": str(crs) if crs else None,
            "crs_available": crs is not None,
            "is_projected": crs.is_projected if crs else False,
            "is_geographic": crs.is_geographic if crs else False,
        }