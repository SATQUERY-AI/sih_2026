import numpy as np


def normalize_raster(raster_data: np.ndarray) -> np.ndarray:
    """
    Normalize raster pixel values to the range [0, 1].

    Expected input shape:
        [bands, height, width]
    """

    data = raster_data.astype(np.float32)

    min_value = data.min()
    max_value = data.max()

    if max_value == min_value:
        return np.zeros_like(data, dtype=np.float32)

    normalized = (data - min_value) / (max_value - min_value)

    return normalized