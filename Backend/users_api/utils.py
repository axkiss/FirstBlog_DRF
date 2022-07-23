from PIL import Image

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator


def send_email_for_verify(request, user):
    """
    Sending email with link for verify user email address
    :param request:
    :param user:
    :return:
    """
    email_template_name = 'users_api/email_confirm_email.html',
    # SeoData = apps.get_model('blog_app', 'SeoData')
    # seo_data = SeoData.objects.first()
    # if seo_data:
    #     site_name = seo_data.site_name
    #     domain = seo_data.domain
    # else:
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain
    context = {
        'domain': domain,
        'site_name': site_name,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': token_generator.make_token(user),
        'protocol': request.scheme,
    }

    message = render_to_string(email_template_name, context=context)
    email = EmailMessage(f'Verify email - {site_name}',
                         message,
                         to=[user.email],
                         )
    email.send()


def crop_img_to_square(image):
    """
    Crop 'PIL.Image.Image` object to square
    :param image: 'PIL.Image.Image` object
    :return: 'PIL.Image.Image` object
    """
    if image.width != image.height:
        # crop to center square
        min_side = min(image.width, image.height)
        if min_side == image.height:
            start_point = int((image.width - image.height) // 2)
            area = (start_point, 0, start_point + image.height, image.height)
            image = image.crop(area)
        else:
            start_point = int((image.height - image.width) // 2)
            area = (0, start_point, image.width, start_point + image.width)
            image = image.crop(area)
    return image


def make_square_img(height_side, img_path):
    """
    Crop to square and resize
    :param height_side:
    :param img_path:
    :return:
    """
    pic = Image.open(img_path)
    pic = crop_img_to_square(pic)
    if not (pic.width == pic.height == height_side):
        # resize
        pic.thumbnail((height_side, height_side), Image.LANCZOS)
        pic.save(img_path)
