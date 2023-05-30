from dotenv import load_dotenv
import os
import interactions
from interactions import slash_command, SlashContext, slash_option, OptionType, Button,ActionRow, ButtonStyle, listen,Client
from interactions.api.events import Component
import random

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
win_url="https://cdn5.vectorstock.com/i/1000x1000/20/74/you-win-poster-with-prize-cup-vector-17052074.jpg"
lose_url="https://cdn5.vectorstock.com/i/1000x1000/16/84/you-lose-game-screen-slot-machine-lottery-concept-vector-44381684.jpg"
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


    """                 BUTTONS             """
    global bt_H,bt_T
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

    """                 EMBEDS              """
    global win_embeds, lose_embeds
    win_embeds = interactions.Embed(
                title="WIN",
                description="You Win",
                color=0x2C7F1A,
            )
    lose_embeds = interactions.Embed(
                title="LOSE",
                description="you lose",
                color=0xFF5733)
    win_embeds.set_image(
                url=win_url)
    lose_embeds.set_image(
                url=lose_url)

    """                 USER PROFILE        """
    @slash_command(name="profile", description="User's Info")
    async def profile(self,ctx: SlashContext):
        avatar = ctx.author.avatar_url
        await ctx.send(avatar)

    """                 COIN FLIPPER          """
    @slash_command(name="flip", description="CoinFlipper)")
    @slash_option(
        name="integer_option",
        description="Integer Option",
        required=True,
        opt_type=OptionType.INTEGER,
    )
    async def flip(self,ctx: SlashContext, integer_option: int):
        components: list[ActionRow] = [ActionRow(bt_T,bt_H)]
        await ctx.send(components=components)

    """                 BUTTON'S ACTION         """
    @listen()
    async def on_component(self,event: Component):
            ctx = event.ctx
            match ctx.custom_id:
                case "tail":
                    user_coin='tail'
                    if ('head' if random.random() < (lambda user_coin: COEFF if (user_coin == 'head') else 1-COEFF)(
                            user_coin=user_coin) else 'tail') == user_coin:
                        await ctx.send(embeds=win_embeds)
                        await ctx.message.delete()
                    else:
                        await ctx.send(embed=lose_embeds)
                        await ctx.message.delete()
                case "head":
                    user_coin = 'head'
                    if ('head' if random.random() < (lambda user_coin: COEFF if (user_coin == 'head') else 1-COEFF)(
                            user_coin=user_coin) else 'tail') ==user_coin:
                        await ctx.send(embeds=win_embeds)
                        await ctx.message.delete()
                    else:
                        await ctx.send(embeds=lose_embeds)
                        await ctx.message.delete()


cl = Game_Bot()
cl.start(discord_token)


