from PIL import Image


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
