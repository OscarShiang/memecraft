from os import getenv

import pyimgur

IMGUR_CLIENT_ID = getenv('IMGUR_CLIENT_ID')

im = pyimgur.Imgur(IMGUR_CLIENT_ID)

def uploadImage(filename, title):
    img = im.upload_image(filename, title=title)
    return img.link