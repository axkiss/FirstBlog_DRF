import os
from unidecode import unidecode

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from .models import Post
from .services import get_unique_slug


@receiver(pre_save, sender=Post)
def make_or_update_slug(sender, instance, **kwargs):
    """Make slug from title"""

    old_title = None
    if instance.id:
        try:
            old_title = sender.objects.get(id=instance.id).title
        except ObjectDoesNotExist:
            return False
    if instance.title != old_title:
        instance.slug = get_unique_slug(instance, max_length=80)


@receiver(pre_save, sender=Post)
def delete_old_image_and_thumbnail(sender, instance, **kwargs):
    """
    Deleting old image, thumbnail if image of post was change
    """
    if not instance.id:
        return False

    try:
        old_image = sender.objects.get(id=instance.id).image
        old_thumbnail = sender.objects.get(id=instance.id).thumbnail
    except ObjectDoesNotExist:
        return False

    # compare image of post and delete the oldest image and thumbnail
    new_image = instance.image
    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
        if os.path.isfile(old_thumbnail.path):
            os.remove(old_thumbnail.path)


@receiver(pre_delete, sender=Post)
def delete_image_and_thumbnail(sender, instance, **kwargs):
    """
    Deleting image, thumbnail with the post on the blog
    """
    image = instance.image
    thumbnail = instance.thumbnail
    if os.path.isfile(image.path):
        os.remove(image.path)
    if os.path.isfile(thumbnail.path):
        os.remove(thumbnail.path)
