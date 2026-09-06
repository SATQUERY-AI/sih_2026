import numpy as np
import rasterio


def validate_quality(file_path: str) -> dict:
    try:
        with rasterio.open(file_path) as src:
            data = src.read()

            total_pixels = data.size
            invalid_pixels = np.count_nonzero(~np.isfinite(data))
            valid_pixels = total_pixels - invalid_pixels

            has_data = total_pixels > 0
            no_invalid_values = invalid_pixels == 0

            valid = has_data and no_invalid_values

            return {
                "valid": valid,
                "total_pixels": int(total_pixels),
                "valid_pixels": int(valid_pixels),
                "invalid_pixels": int(invalid_pixels),
                "checks": {
                    "has_data": has_data,
                    "no_invalid_values": no_invalid_values
                },
                "message": (
                    "Raster quality is acceptable."
                    if valid
                    else "Raster contains invalid or unusable pixel data."
                )
            }

    except Exception as e:
        return {
            "valid": False,
            "message": f"Unable to validate raster quality: {str(e)}"
        }