from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

from users_api.models import User
from users_api.validators import ImageSizeValidator
from .services import create_thumbnail_for_post, get_unique_slug


class Post(models.Model):
    """Posts on blog"""
    title = models.CharField(max_length=100)
    slug = models.SlugField(default='', null=False, db_index=True, max_length=80)
    description = RichTextUploadingField()
    image = models.ImageField(upload_to='post/%Y/%m/%d/',
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                          ImageSizeValidator(min_size=(1200, 900), max_size=(4000, 3000))])
    thumbnail = models.ImageField(upload_to='post/%Y/%m/%d/', editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = TaggableManager()
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    #
    # def get_absolute_url(self):
    #     return reverse('blog:post_detail', args=[self.slug])
    #
    # def add_one_view(self):
    #     Post.objects.filter(id=self.id).update(views=F('views') + 1)
    #     return None
    #
    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(self, max_length=80)
        create_thumbnail_for_post(self, height_side=100)
        super(Post, self).save(*args, **kwargs)
