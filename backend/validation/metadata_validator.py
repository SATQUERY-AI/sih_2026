from pathlib import Path
import rasterio


def validate_metadata(file_path: str) -> dict:
    path = Path(file_path)

    if not path.is_file():
        return {
            "valid": False,
            "message": "Input file does not exist."
        }

    try:
        with rasterio.open(file_path) as src:
            checks = {
                "width": src.width > 0,
                "height": src.height > 0,
                "band_count": src.count > 0,
                "dtype": len(src.dtypes) > 0,
                "crs": src.crs is not None,
                "transform": src.transform is not None,
            }

            valid = all(checks.values())

            return {
                "valid": valid,
                "width": src.width,
                "height": src.height,
                "band_count": src.count,
                "dtype": src.dtypes[0] if src.dtypes else None,
                "crs": str(src.crs) if src.crs else None,
                "checks": checks,
                "message": (
                    "Required raster metadata is valid."
                    if valid
                    else "Required raster metadata is incomplete."
                ),
            }

    except Exception as e:
        return {
            "valid": False,
            "message": f"Unable to read raster metadata: {str(e)}"
        }