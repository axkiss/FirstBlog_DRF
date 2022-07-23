from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


@deconstructible()
class ImageSizeValidator:
    """Compare width and height of img with max and min allowed """
    messages = {
        'big': _('Your img %(img_width)s x %(img_height)s is too big. Max size %(max_width)s x %(max_height)s'),
        'small': _('Your img %(img_width)s x %(img_height)s is too small. Min size %(min_width)s x %(min_height)s'),
    }

    def __init__(self, min_size: tuple = (None, None), max_size: tuple = (None, None), messages: dict = None):
        self.min_width, self.min_height = min_size
        self.max_width, self.max_height = max_size
        if messages is not None and isinstance(messages, dict):
            self.messages = messages

    def __call__(self, img):
        if self.min_width is not None \
                and self.min_height is not None \
                and (img.width < self.min_width or img.height < self.min_height):
            raise exceptions.ValidationError(
                self.messages['small'],
                code="invalid_size",
                params={
                    'min_width': str(self.min_width),
                    'min_height': str(self.min_height),
                    'img_width': str(img.width),
                    'img_height': str(img.height),
                }
            )
        if self.max_width is not None \
                and self.max_height is not None \
                and (img.width > self.max_width or img.height > self.max_height):
            raise exceptions.ValidationError(
                self.messages['big'],
                code="invalid_size",
                params={
                    'max_width': str(self.max_width),
                    'max_height': str(self.max_height),
                    'img_width': str(img.width),
                    'img_height': str(img.height),
                }
            )

    def __eq__(self, other):
        return (
                isinstance(other, self.__class__) and
                self.min_width == other.min_width and
                self.min_height == other.min_height and
                self.max_width == other.max_width and
                self.max_height == other.max_height
        )


def password_validator(password: str, user, password2: str | None = None):
    """Validate whether the password meets all standard django validator requirements"""
    errors = []
    if password != password2 and password2 is not None:
        errors.append('Password is not equal.')
    try:
        validate_password(password=password, user=user)
    except exceptions.ValidationError as ex:
        errors.extend(ex.messages)
    if errors:
        raise serializers.ValidationError({'password': errors})
