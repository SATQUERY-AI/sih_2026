import rasterio


def read_raster(file_path: str):
    """
    Read a GeoTIFF/TIFF raster.

    Returns:
        raster_data: Raster values as a NumPy array
        profile: Raster metadata/profile
    """

    with rasterio.open(file_path) as src:
        raster_data = src.read()
        profile = src.profile.copy()

    return raster_data, profile


def get_raster_info(file_path: str) -> dict:
    """
    Extract basic raster information.
    """

    with rasterio.open(file_path) as src:
        return {
            "width": src.width,
            "height": src.height,
            "band_count": src.count,
            "dtype": src.dtypes[0],
            "crs": str(src.crs) if src.crs else None,
            "transform": str(src.transform),
            "driver": src.driver,
        }