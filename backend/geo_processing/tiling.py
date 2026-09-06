import rasterio
from rasterio.windows import Window


def tile_raster(
    input_path: str,
    output_dir: str,
    tile_size: int = 128
):
    """
    Split a raster into smaller tiles.

    The original raster is not modified.
    """

    if tile_size <= 0:
        raise ValueError("Tile size must be greater than 0.")

    output_dir_path = __import__("pathlib").Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    tile_paths = []

    with rasterio.open(input_path) as src:

        tile_number = 1

        for row in range(0, src.height, tile_size):
            for col in range(0, src.width, tile_size):

                width = min(tile_size, src.width - col)
                height = min(tile_size, src.height - row)

                window = Window(col, row, width, height)

                data = src.read(window=window)

                transform = src.window_transform(window)

                profile = src.profile.copy()
                profile.update(
                    width=width,
                    height=height,
                    transform=transform
                )

                output_path = (
                    output_dir_path / f"tile_{tile_number:03d}.tif"
                )

                with rasterio.open(output_path, "w", **profile) as dst:
                    dst.write(data)

                tile_paths.append(str(output_path))
                tile_number += 1

    return tile_paths