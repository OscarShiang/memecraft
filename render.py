from urllib.request import urlopen

from PIL import Image, ImageDraw, ImageFont


def renderImage(url, texts, configs, font_family, fontsize, color):
    img = Image.open(urlopen(url))
    img_edit = ImageDraw.Draw(img)

    for text, config in zip(texts, configs):
        font = ImageFont.truetype(font_family, fontsize)
        width, height = font.getsize(text)
        img_edit.text((config[0] - width / 2, config[1] - height / 2), text, color, font=font)

    img.save('upload.png')

def renderImageWithOutline(url, texts, configs, font_family, fontsize, color, color_out):
    img = Image.open(urlopen(url))
    img_edit = ImageDraw.Draw(img)

    for text, config in zip(texts, configs):
        font = ImageFont.truetype(font_family, fontsize)
        width, height = font.getsize(text)
        img_edit.text((config[0] - width / 2, config[1] - height / 2), text, color_out, font=font, stroke_width=round(fontsize / 24), stroke_fill=color_out)
        img_edit.text((config[0] - width / 2, config[1] - height / 2), text, color, font=font)

    img.save('upload.png')