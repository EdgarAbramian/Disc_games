from PIL import Image, ImageDraw



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
    size = (500, 500)
    def ava_to_circ(self):
        im = Image.open('../profile/avatar.png')
        im =self.crop(im, size)
        im.putalpha(self.prepare_mask(size, 4))
        im.save('circ_ava.png')


















