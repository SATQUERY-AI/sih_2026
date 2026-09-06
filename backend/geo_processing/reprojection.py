
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling


def reproject_raster(input_path: str, output_path: str, target_crs: str):
    """
    Reproject a raster to the requested CRS.

    If the raster already uses the target CRS, no reprojection is performed.
    """

    with rasterio.open(input_path) as src:

        source_crs = src.crs

        if source_crs is None:
            raise ValueError("Input raster has no CRS.")

        if str(source_crs) == target_crs:
            raise ValueError(
                f"Input raster is already in {target_crs}. "
                "Reprojection is not required."
            )

        transform, width, height = calculate_default_transform(
            source_crs,
            target_crs,
            src.width,
            src.height,
            *src.bounds
        )

        profile = src.profile.copy()

        profile.update(
            crs=target_crs,
            transform=transform,
            width=width,
            height=height
        )

        with rasterio.open(output_path, "w", **profile) as dst:

            for band in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, band),
                    destination=rasterio.band(dst, band),
                    src_transform=src.transform,
                    src_crs=source_crs,
                    dst_transform=transform,
                    dst_crs=target_crs,
                    resampling=Resampling.bilinear
                )

    return output_path