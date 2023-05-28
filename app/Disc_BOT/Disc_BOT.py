from dotenv import load_dotenv
import os
import interactions
from interactions import slash_command, SlashContext, slash_option, OptionType, Button,ActionRow, ButtonStyle, listen
from interactions.api.events import Component
from app.CoinlFlpper.CoinFlipper import flip
load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
import random

COEFF = 0.2

bot = interactions.Client()

globals()
bt_H = Button(
        custom_id='head',
        style=ButtonStyle.GREEN,
        label="Head",
        disabled= False
    )
globals()
bt_T = Button(
        custom_id='tail',
        style=ButtonStyle.GREEN,
        label="Tail",
    )
@slash_command(name="my_command", description="My first command :)")
@slash_option(
    name="integer_option",
    description="Integer Option",
    required=True,
    opt_type=OptionType.INTEGER,

)

async def flip(ctx: SlashContext, integer_option: int):


    components: list[ActionRow] = [ActionRow(bt_T,bt_H)]

    await ctx.send(components=components)

@listen()
async def on_component(event: Component):
        win_embeds = interactions.Embed(
            title="WIN",
            description="You Win",
            color=0x2C7F1A,
        )
        win_embeds.set_image(
            url="attachment://img/big-win-gambling-games-banner-with-win-vector-17338142.webp")
        lose_embeds = interactions.Embed(
            title="LOSE",
            description="you lose",
            color=0xFF5733)
        # lose_embeds.set_image(
        #     url='game-over-games-screen-glitch-computer-video-vector-22579464.webp')

        ctx = event.ctx

        match ctx.custom_id:
            case "tail":
                bt_H.disabled = True
                user_coin='tail'#'head' if random.random() <( lambda user_coin :  0.2 if(user_coin == 'head')  else 0.8)(user_coin = user_coin) else 'tail'
                if ('head' if random.random() < (lambda user_coin: 0.2 if (user_coin == 'head') else 0.8)(
                        user_coin=user_coin) else 'tail') == user_coin:
                    await ctx.send(embeds=win_embeds)
                else:

                    await ctx.send(embeds=lose_embeds)
            case "head":
                bt_H.disabled = True
                user_coin = 'head'
                if ('head' if random.random() < (lambda user_coin: 0.2 if (user_coin == 'head') else 0.8)(
                        user_coin=user_coin) else 'tail') ==user_coin:
                    await ctx.send(embeds=win_embeds)
                else:
                    await ctx.send(embeds=lose_embeds)



bot.start(discord_token)
