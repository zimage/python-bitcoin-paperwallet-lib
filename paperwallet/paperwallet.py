#!/usr/bin/python
# -*- coding: utf-8 -*-
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps
import qrcode
from qrcode import constants


class PaperWallet(object):

    def __init__(
        self,
        config_filename,
        image_filename,
        public_key,
        private_key,
        ):
        config = {}
        execfile(config_filename, config)

        self.image = Image.open(image_filename)

        for i in config['public_key']:
            i.setdefault('color', (0, 0, 0))
            i.setdefault('rotate', 0)

            if i['type'] == 'text':
                font = \
                    ImageFont.truetype('/Library/Fonts/Arial Bold.ttf',
                        i['font-size'])
                self.add_text(public_key, i['location'], color=i['color'
                              ], font=font, rotate=i['rotate'])
            if i['type'] == 'qr':
                self.add_qr(public_key, i['location'], i['scale'])

        for i in config['private_key']:
            i.setdefault('color', (0, 0, 0))
            i.setdefault('rotate', 0)

            if i['type'] == 'text':
                font = \
                    ImageFont.truetype('/Library/Fonts/Arial Bold.ttf',
                        i['font-size'])
                self.add_text(private_key, i['location'],
                              color=i['color'], font=font,
                              rotate=i['rotate'])
            if i['type'] == 'qr':
                self.add_qr(private_key, i['location'], i['scale'])

    def save(self, filename):
        self.image.save(filename)

    def add_text(
        self,
        data,
        location,
        font=None,
        font_size=13,
        color=(0, 0, 0),
        rotate=0,
        ):
        if font is None:
            font = ImageFont.truetype('/Library/Fonts/Arial.ttf',
                    font_size)
        text = Image.new('L', font.getsize(data))
        d = ImageDraw.Draw(text)
        d.text((0, 0), data, font=font, fill=255)
        t = text.rotate(rotate, expand=1)
        self.image.paste(ImageOps.colorize(t, (0, 0, 0), color), location, t)

    def add_qr(
        self,
        data,
        location,
        scale=2,
        ):
        qr = qrcode.QRCode(version=1,
                           error_correction=constants.ERROR_CORRECT_H,
                           box_size=1)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image()
        img = img.resize((int(img.size[0] * scale), int(img.size[1]
                         * scale)), PIL.Image.ANTIALIAS)
        self.image.paste(img, location)


