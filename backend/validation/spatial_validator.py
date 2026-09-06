import rasterio


def validate_spatial(file_path: str) -> dict:
    try:
        with rasterio.open(file_path) as src:
            crs_valid = src.crs is not None
            transform_valid = src.transform is not None
            bounds_valid = (
                src.bounds.left < src.bounds.right
                and src.bounds.bottom < src.bounds.top
            )

            valid = crs_valid and transform_valid and bounds_valid

            return {
                "valid": valid,
                "crs": str(src.crs) if src.crs else None,
                "bounds": {
                    "left": src.bounds.left,
                    "bottom": src.bounds.bottom,
                    "right": src.bounds.right,
                    "top": src.bounds.top,
                },
                "checks": {
                    "crs": crs_valid,
                    "transform": transform_valid,
                    "bounds": bounds_valid,
                },
                "message": (
                    "Spatial information is valid."
                    if valid
                    else "Spatial information is incomplete or invalid."
                ),
            }

    except Exception as e:
        return {
            "valid": False,
            "message": f"Unable to read spatial information: {str(e)}"
        }