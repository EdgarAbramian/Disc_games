from PIL import Image
from app.Profile_Photo.circ_ava.ava import ava

ava = ava()
ava.ava_to_circ()

im1 = Image.open('background.png')
im2 = Image.open('circ_ava.png')

# im1.paste(im2, (800, 150))
# im1.save('profile.png', quality=95)

text_img = Image.new('RGBA', (im1.size), (0, 0, 0, 0))
text_img.paste(im1)
text_img.paste(im2,(800, 150) ,mask=im2)
text_img.save("profile.png", format="png")

im1.close()
im2.close()