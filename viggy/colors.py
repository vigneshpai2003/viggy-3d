def fromRGB(rgb: str):
    """
    convert rgb string to 3 element list suitable for passing to OpenGL
    """
    return [int(rgb[2 * i: 2 * i + 2], 16) / 255 for i in range(3)]


# TODO: add more color conversions and tools
