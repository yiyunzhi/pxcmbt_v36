# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_icon_repo.py
# ------------------------------------------------------------------------------
#
# File          : class_icon_repo.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import os, wx, json
import wx.svg as wsvg
from PIL import Image, ImageFont, ImageDraw
from .define import THIS_RESOURCES_PATH


class IconRepoException(Exception):
    pass


class IconRepoCategory:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self._cache = None

    def get_bmp(self, **kwargs):
        pass


class IconRepo:
    def __init__(self):
        self._categories = dict()

    @property
    def categories(self)->dict:
        return self._categories

    def register(self, item: IconRepoCategory):
        if item.name in self._categories:
            raise IconRepoException('IconRepoCategory %s already exist' % item.name)
        self._categories.update({item.name: item})

    def unregister(self, name):
        if name in self._categories:
            self._categories.pop(name)

    def get_bmp(self, **kwargs):
        if 'category' not in kwargs:
            return None
        _cate = kwargs.pop('category')
        if _cate not in self._categories:
            raise IconRepoException('IconRepoCategory %s not exist' % _cate)
        return self._categories[_cate].get_bmp(**kwargs)


class LocalIconRepoCategory(IconRepoCategory):
    def __init__(self, **kwargs):
        IconRepoCategory.__init__(self, **kwargs)
        # required files dictionary {name: path}
        self._files = kwargs.get('files', dict())
        self._cache = dict()

    def get_bmp(self, **kwargs):
        _name = kwargs.get('name')
        if _name is None or _name not in self._files:
            return wx.NullBitmap
        _color = kwargs.get('color')
        _size: wx.Size = kwargs.get('size',wx.Size(-1,-1))
        _w, _h = _size.GetWidth(), _size.GetHeight()
        if _w == -1:
            _w = 16
        if _h == -1:
            _h = 16
        _cache_key = hash(((_w, _h), _name, _color))
        if _cache_key in self._cache:
            return wx.Bitmap(self._cache.get(_cache_key))
        _path = self._files.get(_name)
        if not os.path.exists(_path):
            return wx.NullBitmap
        _, _ext = os.path.splitext(_path)
        if _ext.lower() == '.svg':
            _img: wsvg.SVGimage = wsvg.SVGimage.CreateFromFile(_path)
            _bmp = _img.ConvertToScaledBitmap(wx.Size(_w, _h))
        elif _ext.lower()=='.xpm':
            _bmp = wx.Bitmap(_path, wx.BITMAP_TYPE_XPM)
            _bmp.Rescale(_bmp, wx.Size(_w, _h))
        elif _ext.lower()=='.png':
            _bmp = wx.Bitmap(_path, wx.BITMAP_TYPE_PNG)
            _bmp.Rescale(_bmp, wx.Size(_w, _h))
        else:
            _bmp = wx.Bitmap(_path, wx.BITMAP_TYPE_ANY)
            _bmp.Rescale(_bmp,wx.Size(_w,_h))
        self._cache.update({_cache_key: _bmp})
        return wx.Bitmap(_bmp)


class FontIconIconRepoCategory(IconRepoCategory):
    FI_COD_ICON = 1
    FI_ELUSIVE_ICON = 2
    FI_FONTAWESOME47 = 3
    FI_FONTAWESOME5_BRAND = 4
    FI_FONTAWESOME5_REGULAR = 5
    FI_FONTAWESOME5_SOLID = 6
    FI_MATERIAL_DESIGN_ICON5 = 7
    FI_MATERIAL_DESIGN_ICON6 = 8
    FI_PHOSPHOR = 9
    FI_REMIX_ICON = 10

    FI_COD_ICON_PREFIX = 'ci'
    FI_ELUSIVE_ICON_PREFIX = 'ei'
    FI_FONTAWESOME47_PREFIX = 'fa47'
    FI_FONTAWESOME5_BRAND_PREFIX = 'fa5b'
    FI_FONTAWESOME5_REGULAR_PREFIX = 'fa5r'
    FI_FONTAWESOME5_SOLID_PREFIX = 'fa5s'
    FI_MATERIAL_DESIGN_ICON5_PREFIX = 'md5'
    FI_MATERIAL_DESIGN_ICON6_PREFIX = 'md6'
    FI_PHOSPHOR_PREFIX = 'pi'
    FI_REMIX_ICON_PREFIX = 'ri'

    FI_COD_ICON_FACE_NAME = 'codicon'
    FI_ELUSIVE_ICON_FACE_NAME = 'elusiveicons'
    FI_FONTAWESOME47_FACE_NAME = 'FontAwesome'
    FI_FONTAWESOME5_BRAND_FACE_NAME = 'Font Awesome 5 Brands Regular'
    FI_FONTAWESOME5_REGULAR_FACE_NAME = 'Font Awesome 5 Free Regular'
    FI_FONTAWESOME5_SOLID_FACE_NAME = 'Font Awesome 5 Free Solid'
    FI_MATERIAL_DESIGN_ICON5_FACE_NAME = 'Material Design Icons 5.9.55'
    FI_MATERIAL_DESIGN_ICON6_FACE_NAME = 'Material Design Icons'
    FI_PHOSPHOR_FACE_NAME = 'Phosphor'
    FI_REMIX_ICON_FACE_NAME = 'remixicon'

    def __init__(self, **kwargs):
        _usage = kwargs.pop('usage') if 'usage' in kwargs else None
        IconRepoCategory.__init__(self, **kwargs)
        self._charMap = dict()
        self._cache = dict()
        self._baseSize = 128
        _ret = True
        if _usage is None or self.FI_COD_ICON in _usage:
            _ret &= self._add_local_font('codicon.ttf',
                                         'codicon-charmap.json',
                                         {'faceName': self.FI_COD_ICON_FACE_NAME, 'key': self.FI_COD_ICON_PREFIX})
        if _usage is None or self.FI_ELUSIVE_ICON in _usage:
            _ret &= self._add_local_font('elusiveicons-webfont.ttf',
                                         'elusiveicons-webfont-charmap.json',
                                         {'faceName': self.FI_ELUSIVE_ICON_FACE_NAME, 'key': self.FI_ELUSIVE_ICON_PREFIX})
        if _usage is None or self.FI_FONTAWESOME47 in _usage:
            _ret &= self._add_local_font('fontawesome4.7-webfont.ttf',
                                         'fontawesome4.7-webfont-charmap.json',
                                         {'faceName': self.FI_FONTAWESOME47_FACE_NAME, 'key': self.FI_FONTAWESOME47_PREFIX})
        if _usage is None or self.FI_FONTAWESOME5_BRAND in _usage:
            _ret &= self._add_local_font('fontawesome5-brands-webfont.ttf',
                                         'fontawesome5-brands-webfont-charmap.json',
                                         {'faceName': self.FI_FONTAWESOME5_BRAND_FACE_NAME, 'key': self.FI_FONTAWESOME5_BRAND_PREFIX})
        if _usage is None or self.FI_FONTAWESOME5_REGULAR in _usage:
            _ret &= self._add_local_font('fontawesome5-regular-webfont.ttf',
                                         'fontawesome5-regular-webfont-charmap.json',
                                         {'faceName': self.FI_FONTAWESOME5_REGULAR_FACE_NAME, 'key': self.FI_FONTAWESOME5_REGULAR_PREFIX})
        if _usage is None or self.FI_FONTAWESOME5_SOLID in _usage:
            _ret &= self._add_local_font('fontawesome5-solid-webfont.ttf',
                                         'fontawesome5-solid-webfont-charmap.json',
                                         {'faceName': self.FI_FONTAWESOME5_SOLID_FACE_NAME, 'key': self.FI_FONTAWESOME5_SOLID_PREFIX})
        if _usage is None or self.FI_MATERIAL_DESIGN_ICON5 in _usage:
            _ret &= self._add_local_font('materialdesignicons5-webfont.ttf',
                                         'materialdesignicons5-webfont-charmap.json',
                                         {'faceName': self.FI_MATERIAL_DESIGN_ICON5_FACE_NAME, 'key': self.FI_MATERIAL_DESIGN_ICON5_PREFIX})
        if _usage is None or self.FI_MATERIAL_DESIGN_ICON6 in _usage:
            _ret &= self._add_local_font('materialdesignicons6-webfont.ttf',
                                         'materialdesignicons6-webfont-charmap.json',
                                         {'faceName': self.FI_MATERIAL_DESIGN_ICON6_FACE_NAME, 'key': self.FI_MATERIAL_DESIGN_ICON6_PREFIX})
        if _usage is None or self.FI_PHOSPHOR in _usage:
            _ret &= self._add_local_font('phosphor.ttf',
                                         'phosphor-charmap.json',
                                         {'faceName': self.FI_PHOSPHOR_FACE_NAME, 'key': self.FI_PHOSPHOR_PREFIX})
        if _usage is None or self.FI_REMIX_ICON in _usage:
            _ret &= self._add_local_font('remixicon.ttf',
                                         'remixicon-charmap.json',
                                         {'faceName': self.FI_REMIX_ICON_FACE_NAME, 'key': self.FI_REMIX_ICON_PREFIX})
        assert _ret, SystemError('can not add local font file completely.')

    def _add_local_font(self, font_file, char_map_json_file, meta_info: dict):
        try:
            _font_file = os.path.join(THIS_RESOURCES_PATH, font_file)
            with open(os.path.join(THIS_RESOURCES_PATH, char_map_json_file)) as f:
                self._charMap.update({meta_info.get('key'): {'map': json.load(f),
                                                             'meta': meta_info,
                                                             'fontObject': ImageFont.truetype(_font_file, self._baseSize, encoding='utf-8')}})
            return True
        except Exception as e:
            print('e:', str(e), font_file)
            return False

    @staticmethod
    def pil_image_to_wx_bitmap(pil_image: Image) -> wx.Bitmap:
        return FontIconIconRepoCategory.wx_image_to_wx_bitmap(FontIconIconRepoCategory.pil_image_to_wx_image(pil_image))

    @staticmethod
    def wx_image_to_wx_bitmap(wx_image: wx.Image) -> wx.Bitmap:
        return wx_image.ConvertToBitmap()

    @staticmethod
    def pil_image_to_wx_image(pil_image, copy_alpha=True) -> wx.Image:
        _has_alpha = pil_image.mode[-1] == 'A'
        if copy_alpha and _has_alpha:  # Make sure there is an alpha layer copy.
            _wx_image = wx.Image(*pil_image.size)
            _pil_image_copy_rgba = pil_image.copy()
            _pil_image_copy_rgb = _pil_image_copy_rgba.convert('RGB')  # RGBA --> RGB
            _pil_image_rgb_data = _pil_image_copy_rgb.tobytes()
            _wx_image.SetData(_pil_image_rgb_data)
            _wx_image.SetAlphaBuffer(_pil_image_copy_rgba.tobytes()[3::4])  # Create layer and insert alpha values.

        else:  # The resulting image will not have alpha.
            _wx_image = wx.Image(*pil_image.size)
            _pil_image_copy = pil_image.copy()
            _pil_image_copy_rgb = _pil_image_copy.convert('RGB')  # Discard any alpha from the PIL image.
            _pil_image_rgb_data = _pil_image_copy_rgb.tobytes()
            _wx_image.SetData(_pil_image_rgb_data)
        return _wx_image

    def get_bmp(self, **kwargs) -> wx.Bitmap:
        """
        for converting of image between pillow and wx see the reference:
        https://wiki.wxpython.org/WorkingWithImages
        Args:
            **kwargs:

        Returns: wx.Bitmap

        """
        _name = kwargs.get('name')
        if _name is None:
            return wx.NullBitmap
        _s = _name.split('.')
        _cm = self._charMap.get(_s[0])
        if _cm is None:
            return wx.NullBitmap
        _code: str = _cm['map'].get(_s[1])
        if _code is None:
            return wx.NullBitmap
        _color = kwargs.get('color', '#3f3f3f')
        _size: wx.Size = kwargs.get('size')
        _w, _h = _size.GetWidth(), _size.GetHeight()
        if _w == -1:
            _w = 16
        if _h == -1:
            _h = 16
        _cache_key = hash(((_w, _h), _code, _color))
        if _cache_key in self._cache:
            return wx.Bitmap(self._cache.get(_cache_key))
        _img = Image.new('RGBA', (self._baseSize, self._baseSize), (255, 0, 0, 0))
        _draw = ImageDraw.Draw(_img)
        _font_obj = _cm['fontObject']
        _chr_int = int(_code, 16)
        _draw.text((0, 0), chr(_chr_int), font=_font_obj, fill=_color)
        _img = _img.resize((_w, _h))
        # _img.save('test.png')
        _bmp = self.pil_image_to_wx_bitmap(_img)
        # _bmp.SaveFile('wxbmp.png', wx.BITMAP_TYPE_PNG)
        # store in cache
        self._cache.update({_cache_key: _bmp})
        return wx.Bitmap(_bmp)

    def clear_cache(self):
        self._cache.clear()

    def __get_bmp(self, **kwargs):
        """
        another solution use gcdc, but may not the best way.
        Args:
            **kwargs:

        Returns:

        """
        _name = kwargs.get('name')
        if _name is None:
            return wx.NullBitmap
        _s = _name.split('.')
        _cm = self._charMap.get(_s[0])
        if _cm is None:
            return wx.NullBitmap
        _code: str = _cm['map'].get(_s[1])
        if _code is None:
            return wx.NullBitmap
        _face_name = _cm['meta'].get('faceName')
        _color = kwargs.get('color', '#3f3f3f')
        _mask_color = kwargs.get('mask_color', wx.WHITE)
        _color = wx.Colour(_color)
        _mask_color = wx.Colour(_mask_color)
        _size: wx.Size = kwargs.get('size')
        _w, _h = _size.width, _size.height
        if _w == -1:
            _w = 16
        if _h == -1:
            _h = 16
        _gbmp = wx.Bitmap(_w * 2, _h * 2)
        _ddc = wx.MemoryDC(_gbmp)
        _ddc.Clear()
        # _ddc.SetBackgroundMode(wx.BRUSHSTYLE_TRANSPARENT)
        # _ddc.SetTextBackground(_color)
        # Create graphics context from it
        gcdc = wx.GCDC(_ddc)
        # gcdc.SetBackgroundMode(wx.BRUSHSTYLE_TRANSPARENT)
        # follow comments show the example use difference DC instance to draw the bitmap
        # gc = wx.GraphicsContext.Create(_ddc)
        # gc.SetAntialiasMode(wx.ANTIALIAS_DEFAULT)
        # _ddc.SetFont(wx.Font(wx.FontInfo(min(w, h)-4).FaceName('FontAwesome')))
        # _ddc.DrawText(code, 0, -2)
        # gcdc.SetFont(wx.Font(wx.FontInfo(min(w*2, h*2) - 4*2).FaceName('FontAwesome')))
        gcdc.SetFont(wx.Font(wx.FontInfo(min(_w * 2, _h * 2) - 4 * 2).FaceName(_face_name)))
        gcdc.SetTextForeground(_color)
        # gcdc.SetBrush(wx.TRANSPARENT_BRUSH)
        # gcdc.SetTextBackground(_color)
        # gcdc.SetBackgroundMode(wx.BRUSHSTYLE_TRANSPARENT)
        if _code.startswith('0x'):
            _code = _code[2::]
        _chr_int = int(_code, 16)
        gcdc.DrawText(chr(_chr_int), 0, -2)
        # gc.SetFont(wx.Font(wx.FontInfo(min(w, h) - 4).FaceName('FontAwesome')), wx.Colour('#3f3f3f'))
        # gc.DrawText(code, 0, -2)
        gcdc.Destroy()
        _gbmp.Rescale(_gbmp, wx.Size(_w, _h))
        _gbmp.SetMaskColour(_mask_color)
        return _gbmp
