# Memecraft

## Introduction

`memecraft` is a linebot server for making memes

The basic idea of building this is to make creating memes easy and accessible.

Since the position of the text in a meme can be pre-defined. We can simply enter the content we want and the bot can place the text onto the image.

## Requirements

To run the service locally, you need the following packages. (specific versions can be found in `requirements.txt`)

* `Flask`
* `line-bot-sdk`
* `Pillow`
* `PyImgur`
* `psycopg2`
* `urllib3`
* `graphviz`

## Features

### Making memes

We can use `memecraft` to create memes with the templates. 

You may enter `templates` to view more option of it.

After choosing one template, you only need to send the content you want as a message, then `memecraft` will spawn the image with default configurations.

![](https://i.imgur.com/81kd2BE.jpg)

`memecraft` supports designing so-called grandparents' blessing as well.

We provide several templates for both convention memes and grandparents' blessings.

![](https://i.imgur.com/hiuIvNh.jpg)

### Upload your memes

Feel free to share your meme to others!

`memecraft` supports uploading meme picture from your mobile devices.

You can simply send `upload_image` as the message and upload the image you want to share. Then `memecraft` will save it into the database.

![](https://i.imgur.com/MaCVCyZ.jpg)

### Browse the gallery

`memecraft` stores every result and the memes uploaded from users.

Each time you enter `gallery`, it will retrieve the last 10 images from the database and display them.

![](https://i.imgur.com/ArLWQtf.jpg)

If you are interested in the one in the gallery, you can click it and the bot will send the image to you.

![](https://i.imgur.com/YMZe0YP.jpg)

### More usages

You can send `usage` as the message and see more.

## State diagram

![](https://memecraft-bot.herokuapp.com/show_fsm)

## Try it

Enjoy making memes with `memecraft`!

![](https://i.imgur.com/IBCMPbl.png)