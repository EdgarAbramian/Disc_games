from dotenv import load_dotenv
import os
import interactions
from interactions import slash_command, SlashContext, slash_option, OptionType, Button, ActionRow, ButtonStyle, listen
from interactions.api.events import Component
import random
import requests
import shutil
from PIL import Image, ImageDraw, ImageFilter
from app.database.db import DataBase

global AMOUNT
X_AMOUNT = 1.5


load_dotenv()

"""                 Database variable               """
Data_Base = DataBase()

discord_token = os.getenv('DISCORD_TOKEN')

'''         probability
   if the user has chosen heads then the 
   probability of getting user's coin will be COEFF
   probability of getting the opposite is equal 1-COEFF
   COEFF sets the probability
   flip makes a decision('H' or 'T') based on COEFF
        '''
COEFF = 0.2

bot = interactions.Client()

"""                 BUTTONS             """
bt_H = Button(
    custom_id='head',
    style=ButtonStyle.GREEN,
    label="Head",
)

bt_T = Button(
    custom_id='tail',
    style=ButtonStyle.GREEN,
    label="Tail",
)

"""                 USER PROFILE        """
@slash_command(name="profile", description="User's Info")
async def profile(ctx: SlashContext):
    avatar_url = ctx.author.avatar_url
    res = requests.get(avatar_url, stream=True)
    if res.status_code == 200:
        with open("../Profile_Photo/circ_ava/avatar.png", 'wb') as f:
            shutil.copyfileobj(res.raw, f)
    else:
        pass
    im1 = Image.open('../Profile_Photo/circ_ava/background.png')
    im2 = Image.open('../Profile_Photo/circ_ava/avatar.png')
    mask_im = Image.new("L", im2.size, 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((200, 10, 270, 180), fill=255)
    mask_im_blur = mask_im.filter(ImageFilter.GaussianBlur(10))

    im1.paste(im2, (0, 0), mask_im_blur)
    im1.save('profile.png', quality=95)

    im1.close()
    im2.close()
    mask_im.close()

    await ctx.channel.send(avatar_url)

"""                 COIN FLIPPER          """
@slash_command(name="flip", description="CoinFlipper)")
@slash_option(
    name="amount",
    description="amount",
    required=True,
    opt_type=OptionType.INTEGER,
    min_value=1,
)


async def flip(ctx: SlashContext, amount: int):
    await ctx.defer(ephemeral=True)
    balance_embed = interactions.Embed(
        title="Balance is insufficient " + "Your balance: "+ str(Data_Base.get_balance(ctx.user.id)),
        color=0xF0C43F,
    )
    global AMOUNT
    AMOUNT = amount

    if (amount <= Data_Base.get_balance(ctx.author.id)):
        components: list[ActionRow] = [ActionRow(bt_T, bt_H)]
        await ctx.send(components=components, ephemeral=False)
    else:
        await ctx.send(embed=balance_embed)


"""                 BUTTON'S ACTION         """


@listen()
async def on_component(event: Component):
    ctx = event.ctx
    win_embeds = interactions.Embed(
        title="YOU WON!\nYour balance:" + str(Data_Base.get_balance(ctx.user.id)),
        color=0x2C7F1A,
    )
    lose_embeds = interactions.Embed(
        title="LOSE\nYour balance: " + str(Data_Base.get_balance(ctx.user.id)),
        color=0xFF5733,
    )
    win_embeds.set_thumbnail(
        url="attachment://win.png")
    lose_embeds.set_thumbnail(
        url="attachment://lose.png"
    )


    bt_T.disabled, bt_H.disabled = True, True
    components: list[ActionRow] = [ActionRow(bt_T, bt_H)]
    lose = interactions.File(file_name="lose.png", file="lose.png")
    win = interactions.File(file_name="win.png", file="win.png")
    match ctx.custom_id:
        case "tail":
            user_coin = 'tail'
            if ('head' if random.random() < (lambda user_coin: COEFF if (user_coin == 'head') else 1 - COEFF)(
                    user_coin=user_coin) else 'tail') == user_coin:
                await ctx.send('win')
            else:
                await ctx.send('lose')
            #     Data_Base.add_cash(ctx.author.id, AMOUNT * X_AMOUNT)
            #     await ctx.send(embeds=win_embeds, file=win,ephemeral=False)
            #     await ctx.message.edit(components=components)
            #     bt_T.disabled, bt_H.disabled = False, False
            # else:
            #     Data_Base.minus_cash(ctx.author.id, AMOUNT)
            #     await ctx.send(embeds=lose_embeds,file=lose,ephemeral=False)
            #     await ctx.message.edit(components=components)
            #     bt_T.disabled, bt_H.disabled = False, False
        case "head":
            await ctx.send('tail')
            # user_coin = 'head'
            # if ('head' if random.random() < (lambda user_coin: COEFF if (user_coin == 'head') else 1 - COEFF)(
            #         user_coin=user_coin) else 'tail') == user_coin:
            #     Data_Base.add_cash(ctx.author.id, AMOUNT * X_AMOUNT)
            #     await ctx.send(embeds=win_embeds, file=win, ephemeral=False)
            #     await ctx.message.edit(components=components)
            #     bt_T.disabled, bt_H.disabled = False, False
            # else:
            #     Data_Base.minus_cash(ctx.author.id, AMOUNT)
            #     await ctx.send(embeds=lose_embeds, file=lose, ephemeral=False)
            #     await ctx.message.edit(components=components)
            #     bt_T.disabled, bt_H.disabled = False, False
                # await ctx.message.delete()
"""
                        CoinFlipper algorithm
COEFF = lambda user_coin :  0.2 if(user_coin == 'head')  else 0.
flip = lambda user_coin: 'head' if random.random() < COEFF(user_coin = user_coin) else 'tail'

"""

bot.start(discord_token)
