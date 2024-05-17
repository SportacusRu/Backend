from PIL import Image
from PIL.Image import Resampling
 
def make_thumbnail(filename, size=(512, 512)):
    img = Image.open(filename)
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
    return img