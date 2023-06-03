import emoji
from dotenv import load_dotenv
import os
import interactions
from interactions import slash_command, SlashContext, slash_option, OptionType, Button, ActionRow, ButtonStyle, listen, \
    Client, component_callback, ComponentContext
from interactions.api.events import Component
import random
from app.database.db import DataBase

global AMOUNT
X_RATE = 1.5

Data_Base = DataBase()

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')


class Game_Bot(Client):
    '''         probability
       if the user has chosen heads then the 
       probability of getting user's coin will be COEFF
       probability of getting the opposite is equal 1-COEFF
       COEFF sets the probability
       flip makes a decision('H' or 'T') based on COEFF
            '''
    global COEFF
    COEFF = 0.2

    global win_embeds, lose_embeds, lose, win, head, tail, recharge_balance

    lose = interactions.File(file_name="app/Disc_BOT/lose.png", file="app/Disc_BOT/lose.png")
    win = interactions.File(file_name="app/Disc_BOT/win.png", file="app/Disc_BOT/win.png")

    """                 BUTTONS             """
    head = Button(style=ButtonStyle.BLURPLE, label='head', custom_id="head")
    tail = Button(style=ButtonStyle.GREEN, label='tail', custom_id="tail")
    recharge_balance = Button(style=ButtonStyle.BLUE, emoji="💲", label='Recharge balance', custom_id="recharge_balance")

    """                 USER PROFILE        """

    @slash_command(name="profile", description="User's Info")
    async def profile(self, ctx: SlashContext):
        avatar = ctx.author.avatar_url
        await ctx.send(avatar)

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
                Data_Base.get_balance(ctx.user.id)),
            color=0xF0C43F
        )
        global AMOUNT, head, tail, recharge_balance
        AMOUNT = amount
        if (amount > Data_Base.get_balance(ctx.author.id)):
            await ctx.send(embed=balance_embed, components=[recharge_balance], ephemeral=True)
        else:

            await ctx.send(components=[head, tail], ephemeral=True)

    """                 BUTTON'S ACTION         """

    @component_callback("tail", "head")
    async def my_callback(self, ctx: ComponentContext):

        global win_embeds, lose_embeds, lose, win
        user_coin = ctx.custom_id
        win_embeds = interactions.Embed(
            title="💸💸💸YOU WON!💸💸💸\n    Your balance : " + str(Data_Base.get_balance(ctx.user.id)),
            color=0x2C7F1A,
        )
        lose_embeds = interactions.Embed(
            title="⛔️⛔️📈YOU LOSE⛔️⛔️📈\n    Your balance : " + str(Data_Base.get_balance(ctx.user.id)),
            color=0xFF5733,
        )
        win_embeds.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/1055531650148220948/ee9c8061cbdee30372883dd74f490e5f.png?size=1024")
        lose_embeds.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/965863987411570698/ee184cd0603dfc2d1e0808fbbd23919d.png?size=1024"
        )
        if ('head' if random.random() < (lambda user_coin: COEFF if (user_coin == 'head') else 1 - COEFF)(
                user_coin=user_coin) else 'tail') == user_coin:
            Data_Base.add_cash(ctx.author.id, AMOUNT * X_RATE)
            await ctx.send(embed=win_embeds)
        else:
            Data_Base.minus_cash(ctx.author.id, AMOUNT)
            await ctx.send(embed=lose_embeds)

    """
                            CoinFlipper algorithm
    COEFF = lambda user_coin :  0.2 if(user_coin == 'head')  else 0.8
    flip = lambda user_coin: 'head' if random.random() < COEFF(user_coin = user_coin) else 'tail'
    """


cl = Game_Bot()
