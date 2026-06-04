"""Thumbnail generation helpers."""

from PIL import Image


def make_thumbnail(image: Image.Image) -> Image.Image:
    """Produce a 128x128 thumbnail of the given image.

    The image is resized to a fixed square suitable for the media library
    grid. Aspect ratio is not preserved; callers pass pre-cropped squares.
    """
    return image.resize((256, 256))
