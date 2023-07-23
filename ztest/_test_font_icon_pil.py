# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : _test_font_icon_pil.py
# ------------------------------------------------------------------------------
#
# File          : _test_font_icon_pil.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import wx
from PIL import Image, ImageFont, ImageDraw

def PilRGBA2wxBmp (image):
    width, height = image.size
    return wx.Bitmap.FromBufferAndAlpha(width, height, image.tobytes(),img.getchannel('A').tobytes())


img = Image.new('RGBA', (128, 128), (255, 0, 0, 0))
draw = ImageDraw.Draw(img)
fontObj = ImageFont.truetype('materialdesignicons6-webfont.ttf', 128, encoding = 'utf-8')
#draw.text((0, 0), '\U000f0194', font = fontObj,fill='#000000')
draw.text((0, 0), chr(0xf0194), font = fontObj,fill='#000000')

#img.tobitmap('dw')
img=img.resize((24,24))
bmp=PilRGBA2wxBmp(img)
print(bmp,hash(('pi.dd',(24,24),'#010102')))
img.save('test.png')