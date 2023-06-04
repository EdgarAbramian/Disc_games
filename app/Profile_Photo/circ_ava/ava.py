from PIL import Image, ImageDraw, ImageFont
from app.database.db import *



class ava():
    def __init__(self):
        pass
    def prepare_mask(self,size, antialias = 2):
        mask = Image.new('L', (size[0] * antialias, size[1] * antialias), 0)
        ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
        return mask.resize(size, Image.LANCZOS)


    def crop(self,im, s):
        w, h = im.size
        k = w / s[0] - h / s[1]
        if k > 0: im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
        elif k < 0: im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
        return im.resize(s, Image.LANCZOS)
    global size
    size = (280, 280)
    def ava_to_circ(self,id,USER_NAME):
        from app.database.db import DataBase
        Data = DataBase()
        im = Image.open(r'D:\PycharmProject\Disc_games\app\Profile_Photo\circ_ava\avatar.png')
        im1 = Image.open(r'D:\PycharmProject\Disc_games\app\Profile_Photo\circ_ava\background.png')

        im =self.crop(im, size)
        im.putalpha(self.prepare_mask(size, 4))
        im.convert("RGBA")

        prof_template = Image.new('RGBA', (im1.size), (0, 0, 0, 0))
        prof_template.convert('RGBA')
        prof_template.paste(im1)
        prof_template.paste(im, (770, 128),mask = im.split()[3])


        prfile_png = ImageDraw.Draw(prof_template)
        font = ImageFont.truetype(r'D:\PycharmProject\Disc_games\app\Profile_Photo\circ_ava\OctinVintageBRg Bold.ttf', size=70)
        prfile_png.text((650, 400), USER_NAME, font=font)#142022
        prfile_png.text((170, 550), "Balance: "+ str(Data.get_balance(id)), font=font)  # + str(Data.get_balance(id)))
        prfile_png.text((170, 650), "SMS: ", font=font)
        prfile_png.text((170, 750), "TOP: ", font=font)
        prfile_png.text((1200, 550), "ONLINE: ", font=font)
        prfile_png.text((1200, 650), "DONATES: ", font=font)
        prfile_png.text((1200, 750), "CLAN: ", font=font)

        prof_template.save(r'profile.png', format="png")




profile_ = ava()
















