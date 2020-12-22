from PIL import Image, ImageFont, ImageDraw
from urllib.request import urlopen

def renderImage(url, texts, configs, font_family, fontsize, color):
    img = Image.open(urlopen(url))
    img_edit = ImageDraw.Draw(img)

    for text, config in zip(texts, configs):
        font = ImageFont.truetype(font_family, fontsize)
        width, height = font.getsize(text)
        img_edit.text((config[0] - width / 2, config[1] - height / 2), text, color, font=font)

    img.save('upload.png')