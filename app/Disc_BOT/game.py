import time

from dotenv import load_dotenv
import os
import interactions
from interactions import slash_command, SlashContext, slash_option, OptionType, Client, component_callback, ComponentContext
import requests
import random
from interactions import listen
from interactions.api.events import ChannelCreate,VoiceUserJoin,VoiceUserLeave

from app.database.db import DataBase
from app.Profile_Photo.circ_ava.ava import profile_
global AMOUNT
from app.Disc_BOT.Buttons import *
COIN_FLIPPER_RATE = 1.5

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

Data = DataBase()


class Game_Bot(Client):
    '''         probability
       if the user has chosen heads then the 
       probability of getting user's coin will be COEFF
       probability of getting the opposite is equal 1-COEFF
       COEFF sets the probability
       flip makes a decision('H' or 'T') based on COEFF
            '''
    global COEFF,mes
    COEFF = 0.2


    lose = interactions.File(file_name="app/Disc_BOT/lose.png", file="app/Disc_BOT/lose.png")
    win = interactions.File(file_name="app/Disc_BOT/win.png", file="app/Disc_BOT/win.png")



    """                 USER PROFILE        """

    @slash_command(name="profile", description="User's Info")
    async def profile(self, ctx: SlashContext):
        await ctx.defer(ephemeral=False)
        url = ctx.author.avatar_url
        response = requests.get(url)
        if response.status_code == 200:
            with open(r'D:\PycharmProject\Disc_games\app\Profile_Photo\circ_ava\avatar.png', 'wb') as f:
                f.write(response.content)
        profile_.ava_to_circ(ctx.author.id, ctx.author.user.display_name)

        await ctx.send(file=interactions.File(file_name=r'profile.png',
                                              file=r'D:\PycharmProject\Disc_games\profile.png'
                                              ))

    """                 COIN FLIPPER          """

    @slash_command(name="flip", description="CoinFlipper)")
    @slash_option(
        name="amount",
        description="amount",
        required=True,
        opt_type=OptionType.INTEGER,
        min_value=1,
    )
    async def flip(self, ctx: SlashContext, amount: int):
        await ctx.defer()
        balance_embed = interactions.Embed(
            title="🏦💰🪙Balance is insufficient 🪙💰🏦" + "\n                Your balance: " + str(
                Data.get_balance(ctx.user.id)),
            color=0xF0C43F
        )

        global AMOUNT, head, tail, recharge_balance
        AMOUNT = amount

        if (amount > Data.get_balance(ctx.author.id)):
            await ctx.send(embed=balance_embed, components=[recharge_balance])
        else:
            await ctx.send(components=[head, tail])


    """
                            CoinFlipper algorithm
    COEFF = lambda user_coin :  0.2 if(user_coin == 'head')  else 0.8
    flip = lambda user_coin: 'head' if random.random() < COEFF(user_coin = user_coin) else 'tail'
    Ваше сообщение не было доставлено. Обычно такое случается, потому что у вас нет общих серверов с получателем или получатель принимает личные сообщения только от друзей. 
    Полный перечень причин можно посмотреть здесь: https://support.discord.com/hc/ru/articles/360060145013
    """

    @slash_command(name="roulette", description="roulette)")
    @slash_option(
            name="amount",
            description="amount",
            required=True,
            opt_type=OptionType.INTEGER,
            min_value=1,
    )
    async def roulette(self, ctx: SlashContext, amount: int):
            global mes
            sum = str(amount) + "💲"
            roulette_embed = interactions.Embed(
                title="💸💸💸💸💸💸ROULETTE💸💸💸💸💸💸\n\t\t💰💰💰 Your Bet💰💰💰 : " + sum,
                color=0x2C7F1A,
            ).set_image(
                url="https://thumbs.gfycat.com/DecimalCheerfulAsianlion-size_restricted.gif")
            await ctx.send(components=desk1, embed=roulette_embed)
            mes = ctx.id
            await ctx.send(components=desk2)
            await ctx.send(components=desk3)

    @component_callback("tail", "head")
    async def callback(self, ctx: ComponentContext):
        await ctx.defer(ephemeral=False)
        user_coin = ctx.custom_id
        win_embeds = interactions.Embed(
            title="💸💸💸YOU WON!💸💸💸\n    Your balance : " + str(Data.get_balance(ctx.user.id)),
            color=0x2C7F1A,
        )
        lose_embeds = interactions.Embed(
            title="⛔️⛔️📈YOU LOSE⛔️⛔️📈\n    Your balance : " + str(Data.get_balance(ctx.user.id)),
            color=0xFF5733,
        )
        win_embeds.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/1055531650148220948/ee9c8061cbdee30372883dd74f490e5f.png?size=1024")
        lose_embeds.set_thumbnail(
            url="https://cdn.shopify.com/s/files/1/1280/3657/products/SP-DM-WL_1_1efa82cc-3007-4826-b9d9-e8ee919cb949_800x.jpg")
        # "https://t3.ftcdn.net/jpg/03/12/54/80/360_F_312548010_JsXZ9vxIXTbgZlDr1IwlMTogrN84BN1L.jpg"
        if ('head' if random.random() < (lambda user_coin: COEFF if (user_coin == 'head') else 1 - COEFF)(
                user_coin=user_coin) else 'tail') == user_coin:
            Data.add_cash(ctx.author.id, AMOUNT * COIN_FLIPPER_RATE)
            await ctx.send(embed=win_embeds)
        else:
            Data.minus_cash(ctx.author.id, AMOUNT)
            await ctx.send(embed=lose_embeds)

    @component_callback(btn_id for btn_id in desk_ids)
    async def my_callback(self, ctx: ComponentContext):
        """GENERATING RANDOM NUM """
        num = random.randint(0, 37)

        win_embeds = interactions.Embed(
            title="💸💸💸YOU WON!💸💸💸\n    Your balance : " + str(Data.get_balance(ctx.user.id)),
            color=0x2C7F1A,
        )
        lose_embeds = interactions.Embed(
            title="⛔️⛔️📈YOU LOSE⛔️⛔️📈\n    Your balance : " + str(Data.get_balance(ctx.user.id)),
            color=0xFF5733,
        )
        #        BUTTONS FROM 0 TO 37
        if (ctx.custom_id in desk_num_ids and num == int(ctx.custom_id)):
            await ctx.send(embed=win_embeds)
        #        BUTTONS __1to18__ and __19to37__
        elif((ctx.custom_id == "high" and num <= 18)
                        or (ctx.custom_id == "lower" and num > 18 and num <=37)):
            await ctx.send(embed=win_embeds)
        #       BUTTONS __ODD__ and __EVEN__
        elif ((num % 2 == 0 and ctx.custom_id == "even")
                            or (num % 2 != 0 and ctx.custom_id == "odd")):
            await ctx.send(embed=win_embeds)
        #       BUTTONS __RED__ and __BLACK__
        elif ((ctx.custom_id == "red" and num in red_val)
                    or (ctx.custom_id == "black" and not(num in red_val))):
            await ctx.send(embed=win_embeds)
        #        COIN_FLIPPER
        else:
            channel = await ctx.bot.fetch_channel(ctx.channel_id)
            message = await channel.fetch_message(mes)
            file = interactions.File(r'D:\PycharmProject\Disc_games\app\GIF\out.gif')

            edited_embed = interactions.Embed(
                title="💸💸💸💸💸💸HELLO💸💸💸💸💸💸\n\t\t💰💰💰 Your Bet💰💰💰",
                color=0x2C7F1A,
            ).set_image(url="attachment://out.gif")
            await message.edit(file =file ,embed = edited_embed)
            print(ctx.message.id)
            await ctx.send(embed=lose_embeds)
        # 109105
        print(str(num) + " " + ctx.custom_id)


    """Time spent in voice channel"""
    @listen(VoiceUserJoin)
    async def an_event_VoiceUserJoin(user, event: VoiceUserJoin):
        global t1
        t1 = time.time()
        print(f"VoiceUserJoin: {event.channel.name}, USER:{event.author.id}")
    @listen(VoiceUserLeave)
    async def VoiceUserLeave(user, event: VoiceUserLeave):
        global t2
        t2 = time.time()
        spent = t2-t1
        print(f"VoiceUserLeave: {event.channel.name}, USER:{event.author.user.display_name}, Time Spent:{t2-t1}")
        Data.add_voice(event.author.id, spent)


cl = Game_Bot()
