from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Users on blog"""
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    email_verify = models.BooleanField(default=False)

    # def has_perm_add_post(self):
    #     return self.has_perm('blog_app.add_post')
    #
    # def has_perm_edit_post(self):
    #     return self.has_perm('blog_app.change_post')
    #
    def get_group(self):
        return self.groups.all().first()
    #
    # def get_absolute_url(self):
    #     return reverse('users:profile', args=[self.username])
