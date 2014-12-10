# coding=utf-8
from PIL import Image

"""
Обрезает изображение по центру в соответвии с пропоций
 im - изображение PIL
 crop_height - финальная высота вырезки
 ratio - соотношение сторон вырезки
"""
def image_crop_center(im, crop_height=110, ratio=1.333 ):
    image_width = im.size[0]
    image_height = im.size[1]
    image_ratio = image_width / float(image_height)
    box = [0, 0, 0, 0]
    if image_ratio <= 1:
        new_hight = int(image_width / ratio)
        vert_offset = int((image_height - new_hight) / 2)
        box[0] = 0
        box[1] = vert_offset
        box[2] = image_width
        box[3] = vert_offset + new_hight
    else:
        new_width = image_height * ratio
        if new_width > image_width:
            new_width = image_width
            new_hight = int(new_width / ratio)
            vert_offset = int((image_height - new_hight) / 2)
            box[0] = 0
            box[1] = vert_offset
            box[2] = new_width
            box[3] = vert_offset + new_hight
        else:
            gor_offset = int((image_width - new_width) / 2)
            box[0] = gor_offset
            box[1] = 0
            box[2] = int(gor_offset + new_width)
            box[3] = image_height

    crop_im = im.crop(tuple(box))
    image_ratio = float(crop_im.size[0]) / crop_im.size[1]
    final_width = int((image_ratio * crop_height))
    return crop_im.resize((final_width, crop_height), Image.ANTIALIAS)


"""
Подгоняет изобржаение под заданный размер
"""
def adjust_image(im, max_size):
    image_width = im.size[0]
    image_height = im.size[1]
    image_ratio = image_width / float(image_height)
    new_size = [image_width, image_height]
    if image_width > max_size[0]:
        new_size[0] = max_size[0]
        if image_ratio >= 1:
            new_size[1] = int(max_size[0] / image_ratio)
        else:
            new_size[1] = int(max_size[0] * image_ratio)

    if new_size[1] > max_size[1]:
        new_size[1] = max_size[1]
        if image_ratio >= 1:
            new_size[0] = int(max_size[0] * image_ratio)
        else:
            new_size[0] = int(max_size[0] / image_ratio)

    return im.resize(new_size, Image.ANTIALIAS)