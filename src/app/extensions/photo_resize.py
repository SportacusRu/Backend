from io import BytesIO
from PIL import Image
from PIL.Image import Resampling
from . import get_bytes_from_base64
 
def make_thumbnail(photo, size=(512, 512)):
    buffer = BytesIO()
    photo_data = get_bytes_from_base64(photo)
    img = Image.open(photo_data[0])
    width, height = img.size
    if width > height:
        ratio = width / size[0]
        new_height = int(height / ratio)
        new_size = (size[0], new_height)
    else:
        ratio = height / size[1]
        new_width = int(width / ratio)
        new_size = (new_width, size[1])

    img.thumbnail(new_size, Resampling.LANCZOS)
    img.save(buffer, format=photo_data[1][6:].upper())

    return 