import Crypto.Hash.SHA256 as SHA256
import Crypto.Hash.RIPEMD as RIPEMD160
import hashlib
from bitcoin.key import CKey
import bitcoin.base58

import sys
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps
import qrcode
from qrcode import constants

k = CKey()
k.generate ()
k.set_compressed(False)

def hash_160(public_key):
  h1 = SHA256.new(public_key).digest()
  h2 = RIPEMD160.new(h1).digest()
  return h2

def public_key_to_bc_address(public_key):
  h160 = hash_160(public_key)
  return encode_base58_check(h160)

def private_key_to_wallet_import_format(private_key):
  return encode_base58_check(private_key[9:9+32], version='\x80')

def encode_base58_check(payload, version="\x00"):
  vh160 = version+payload # \x80 is version 80
  h3=SHA256.new(SHA256.new(vh160).digest()).digest()
  addr=vh160+h3[0:4]
  return bitcoin.base58.encode(addr)

public_key = public_key_to_bc_address(k.get_pubkey())
private_key = private_key_to_wallet_import_format(k.get_privkey())

def add_text(data, img, location, font=None, font_size=13, color=(0,0,0), rotate=0,):
    if font is None:
      font = ImageFont.truetype("/Library/Fonts/Arial.ttf", font_size)
    text = Image.new('L', font.getsize(data)) 
    d = ImageDraw.Draw(text)
    d.text((0, 0), data, font=font, fill=255)
    t = text.rotate(rotate, expand=1)
    img.paste( ImageOps.colorize(t, (0,0,0), color), location, t)

def add_qr(data, image, location, scale=2):
    qr = qrcode.QRCode(
        version=1,
        error_correction=constants.ERROR_CORRECT_H,
        box_size=1
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    img = img.resize((int(img.size[0]*scale),int(img.size[1]*scale)), PIL.Image.ANTIALIAS)
    image.paste(img, location)

config = {}
execfile(sys.argv[1], config) 

image = Image.open(sys.argv[2])

for i in config["public_key"]:
  i.setdefault('color', (0,0,0))
  i.setdefault('rotate', 0)

  if i['type'] == "text":
    font = ImageFont.truetype("/Library/Fonts/Arial Bold.ttf", i['font-size'])
    add_text(public_key, image, i['location'], color=i['color'], font=font, rotate=i['rotate'])
  if i['type'] == "qr":
    add_qr(public_key, image, i['location'], i['scale'])

for i in config["private_key"]:
  i.setdefault('color', (0,0,0))
  i.setdefault('rotate', 0)

  if i['type'] == "text":
    font = ImageFont.truetype("/Library/Fonts/Arial Bold.ttf", i['font-size'])
    add_text(private_key, image, i['location'], color=i['color'], font=font, rotate=i['rotate'])
  if i['type'] == "qr":
    add_qr(private_key, image, i['location'], i['scale'])
  
image.save("bar.png")
