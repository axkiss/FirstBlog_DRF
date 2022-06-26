import os
from io import BytesIO
from PIL import Image

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import Q
from django.core.files.base import ContentFile

from users_api.utils import crop_img_to_square


def create_thumbnail_for_post(instance, height_side=100):
    """Create a square thumbnail based of the main image"""
    # If the image of the post did not change --> break
    if instance.thumbnail:
        try:
            old_image = instance.__class__.objects.get(id=instance.id).image
        except ObjectDoesNotExist:
            return
        if instance.image.name == old_image.name:
            return

    # Get name for thumbnail
    thumb_name, thumb_extension = os.path.splitext(instance.image.name)
    thumb_name = os.path.basename(thumb_name)
    thumb_extension = thumb_extension.lower()
    thumb_filename = thumb_name + '_thumb' + thumb_extension

    # Define image file type
    if thumb_extension in ['.jpg', '.jpeg']:
        FTYPE = 'JPEG'
    elif thumb_extension == '.png':
        FTYPE = 'PNG'
    else:
        raise TypeError('Unrecognized image file type')

    # Open, crop and resize image
    pic = Image.open(instance.image)
    pic = crop_img_to_square(pic)
    pic.thumbnail((height_side, height_side), Image.LANCZOS)

    # Save thumbnail to in-memory file as StringIO
    temp_thumb = BytesIO()
    pic.save(temp_thumb, FTYPE)
    temp_thumb.seek(0)

    # set save=False, otherwise it will run in an infinite loop
    instance.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
    temp_thumb.close()


def get_unique_slug(instance, max_length=80):
    """Add to slug now time and make unique"""
    if instance.__class__.objects.filter(Q(slug=instance.slug) & ~Q(id=instance.id)).exists():
        msec = str(timezone.now().microsecond)
        max_length -= len(msec)
        return instance.slug[:max_length] + '-' + msec
    return instance.slug[:max_length]
