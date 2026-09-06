import rasterio
from rasterio.enums import Resampling


def resample_raster(
    input_path: str,
    output_path: str,
    target_resolution: float
):
    """
    Resample a raster to the requested pixel resolution.

    The original raster is not modified.
    """

    if target_resolution <= 0:
        raise ValueError("Target resolution must be greater than 0.")

    with rasterio.open(input_path) as src:

        scale_x = src.res[0] / target_resolution
        scale_y = src.res[1] / target_resolution

        new_width = max(1, round(src.width * scale_x))
        new_height = max(1, round(src.height * scale_y))

        data = src.read(
            out_shape=(src.count, new_height, new_width),
            resampling=Resampling.bilinear
        )

        new_transform = src.transform * src.transform.scale(
            src.width / new_width,
            src.height / new_height
        )

        profile = src.profile.copy()

        profile.update(
            width=new_width,
            height=new_height,
            transform=new_transform
        )

        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(data)

    return output_path