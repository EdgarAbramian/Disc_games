from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys

im1 = Image.open('tatras.jpg')
im2 = Image.open('avatar.png')
mask_im = Image.new("L", im2.size, 0)
draw = ImageDraw.Draw(mask_im)
draw.ellipse((100, 10, 270, 180), fill=255)
mask_im_blur = mask_im.filter(ImageFilter.GaussianBlur(10))

im1.paste(im2, (312, 32), mask_im_blur)
im1.save('profile.jpg', quality=95)

im1.close()
im2.close()
mask_im.close()












