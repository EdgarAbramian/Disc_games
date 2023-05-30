from PIL import Image, ImageDraw, ImageFont
import sys

FONT_PATH = "D:/PycharmProject/Disc_games/app/OctinVintageBRg Bold.ttf"
try:
    tatras = Image.open("tatras.jpg")
except:
    print("Unable to load image")
    sys.exit(1)


idraw = ImageDraw.Draw(tatras)
text = "High Tatras"

font = ImageFont.truetype(FONT_PATH, size=100)

idraw.text((540, 10), text, fill = 'navy',font=font,)

tatras.save('tatras_watermarked.png')












