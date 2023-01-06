from io import BytesIO
from random import randint

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from rembg import remove


def remove_background(image: InMemoryUploadedFile, profile):
    new_image = Image.open(image)
    fp = BytesIO()
    removed_image = remove(new_image)
    removed_image.save(fp, format='PNG')
    return InMemoryUploadedFile(
        fp, None, f'{profile.id}-{image.name}-removed-{randint(1, 100)}.png', 'image/png',
        fp.getbuffer().nbytes, None
    )
