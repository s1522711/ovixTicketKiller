import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='', intents=intents)

ticket_bot_id = int(os.getenv("TICKET_BOT_ID"))
print(type(ticket_bot_id))
moderator_role_id = int(os.getenv("MODERATOR_ROLE_ID"))
print(type(moderator_role_id))

kill_gta_tickets = False
kill_rdr_tickets = False
kill_cs2_tickets = False

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    global kill_gta_tickets
    global kill_rdr_tickets
    global kill_cs2_tickets

    if message.author.id == ticket_bot_id and kill_gta_tickets and '//' in message.content:
        if message.content.split('//')[1].split('//')[0].lower() == 'gta':
            print("found gta ticket")
            await message.channel.send('Hello! the gta category has been disabled!')
            await message.channel.send('$close BOT: GTA CATEGORY DISABLED')
            await message.channel.send('$transcript')
            await message.channel.send('$delete')
    if message.author.id == ticket_bot_id and kill_rdr_tickets and '//' in message.content:
        if message.content.split('//')[1].split('//')[0].lower() == 'rdr' or message.content.split('//')[1].split('//')[0].lower() == 'rdr2':
            print("found rdr ticket")
            await message.channel.send('Hello! the rdr category has been disabled!')
            await message.channel.send('$close BOT: RDR CATEGORY DISABLED')
            await message.channel.send('$transcript')
            await message.channel.send('$delete')
    if message.author.id == ticket_bot_id and kill_cs2_tickets and '//' in message.content:
        if message.content.split('//')[1].split('//')[0].lower() == 'cs2':
            print("found cs2 ticket")
            await message.channel.send('Hello! the cs2 category has been disabled!')
            await message.channel.send('$close BOT: CS2 CATEGORY DISABLED')
            await message.channel.send('$transcript')
            await message.channel.send('$delete')

@bot.tree.command(name="toggle-gta-killing",description="toggle whether to kill gta tickets")
async def slash_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, id=moderator_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        global kill_gta_tickets
        kill_gta_tickets = not kill_gta_tickets
        await interaction.response.send_message("Updated gta killing - " + str(kill_gta_tickets))
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)
    
@bot.tree.command(name="toggle-rdr-killing",description="toggle whether to kill rdr tickets")
async def slash_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, id=moderator_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        global kill_rdr_tickets
        kill_rdr_tickets = not kill_rdr_tickets
        await interaction.response.send_message("Updated rdr killing - " + str(kill_rdr_tickets))
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.tree.command(name="toggle-cs2-killing",description="toggle whether to kill cs2 tickets")
async def slash_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, id=moderator_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        global kill_cs2_tickets
        kill_cs2_tickets = not kill_cs2_tickets
        await interaction.response.send_message("Updated cs2 killing - " + str(kill_cs2_tickets))
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.tree.command(name="killing-status",description="get the status of the ticket killing")
async def slash_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, id=moderator_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("GTA: " + str(kill_gta_tickets) + "\nRDR: " + str(kill_rdr_tickets) + "\nCS2: " + str(kill_cs2_tickets))
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'We have logged in as {bot.user}')


bot.run(DISCORD_TOKEN)
