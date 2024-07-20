import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
DISCORD_TOKEN = os.getenv("TOKEN")
print("token: " + DISCORD_TOKEN)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='', intents=intents)

ticket_bot_id = int(os.getenv("TICKET_BOT_ID"))
print("ticket bot id: " + str(ticket_bot_id))
moderator_role_id = int(os.getenv("MODERATOR_ROLE_ID"))
print("moderator role id: " + str(moderator_role_id))
staff_role_id = int(os.getenv("STAFF_ROLE_ID"))
print("staff role id: " + str(staff_role_id))
trial_staff_role_id = int(os.getenv("TRIAL_STAFF_ROLE_ID"))
print("trial staff role id: " + str(trial_staff_role_id))

kill_gta_tickets = False
kill_rdr_tickets = False
kill_cs2_tickets = False

try:
    with open("last_state.txt", "r") as f:
        kill_gta_tickets = f.readline().strip() == "True"
        kill_rdr_tickets = f.readline().strip() == "True"
        kill_cs2_tickets = f.readline().strip() == "True"
except FileNotFoundError:
    with open("last_state.txt", "w") as f:
        f.write("False\nFalse\nFalse")

print(kill_gta_tickets, kill_rdr_tickets, kill_cs2_tickets)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    global kill_gta_tickets
    global kill_rdr_tickets
    global kill_cs2_tickets

    if message.author.id == ticket_bot_id and kill_gta_tickets and '//' in message.content:
        if 'gta' in message.content.split('//')[1].split('//')[0].lower():
            print("found gta ticket")
            await message.channel.send('Hello! the gta category has been disabled!')
            await message.channel.send('this ticket will be closed in 5 seconds')
            await asyncio.sleep(1)
            for i in range(4):
                await message.channel.send(str(4-i))
                await asyncio.sleep(1)
            await message.channel.send('0 - goodbye!')
            await asyncio.sleep(1)
            await message.channel.send('$close BOT: GTA CATEGORY DISABLED')
            await asyncio.sleep(0.5)
            await message.channel.send('$transcript')
            await asyncio.sleep(0.5)
            await message.channel.send('$delete')
            return
    if message.author.id == ticket_bot_id and kill_rdr_tickets and '//' in message.content:
        if 'rdr' in message.content.split('//')[1].split('//')[0].lower():
            print("found rdr ticket")
            await message.channel.send('Hello! the rdr category has been disabled!')
            await message.channel.send('this ticket will be closed in 5 seconds')
            await asyncio.sleep(1)
            for i in range(4):
                await message.channel.send(str(4-i))
                await asyncio.sleep(1)
            await message.channel.send('0 - goodbye!')
            await asyncio.sleep(1)
            await message.channel.send('$close BOT: RDR CATEGORY DISABLED')
            await asyncio.sleep(0.5)
            await message.channel.send('$transcript')
            await asyncio.sleep(0.5)
            await message.channel.send('$delete')
            return
    if message.author.id == ticket_bot_id and kill_cs2_tickets and '//' in message.content:
        if 'cs' in message.content.split('//')[1].split('//')[0].lower():
            print("found cs2 ticket")
            await message.channel.send('Hello! the cs2 category has been disabled!')
            await message.channel.send('this ticket will be closed in 5 seconds')
            await asyncio.sleep(1)
            for i in range(4):
                await message.channel.send(str(4-i))
                await asyncio.sleep(1)
            await message.channel.send('0 - goodbye!')
            await asyncio.sleep(1)
            await message.channel.send('$close BOT: CS2 CATEGORY DISABLED')
            await asyncio.sleep(0.5)
            await message.channel.send('$transcript')
            await asyncio.sleep(0.5)
            await message.channel.send('$delete')
            return
    message.content.split('//')
    if message.author.id == ticket_bot_id and '//' in message.content and 'pswrd' in message.content.split('//')[1].lower():
        if 'ye' not in message.content.split('//')[2].lower():
            print("found invalid unverified password reset ticket")
            await message.channel.send('Hello! these tickets are only for requesting a password reset for your account!')
            await message.channel.send('this ticket will be closed in 5 seconds')
            await asyncio.sleep(1)
            for i in range(4):
                await message.channel.send(str(4-i))
                await asyncio.sleep(1)
            await message.channel.send('0 - goodbye!')
            await asyncio.sleep(1)
            await message.channel.send('$close BOT: UNVERIFIED PASSWORD RESET IDIOT')
            await asyncio.sleep(0.5)
            await message.channel.send('$transcript')
            await asyncio.sleep(0.5)
            await message.channel.send('$delete')
            return
    if message.author.id == ticket_bot_id and '//' in message.content:
        await message.channel.send('||<@&' + str(staff_role_id) + '> <@&' + str(trial_staff_role_id) + '>||'
                                   '\nPlease do not ping staff, we will get to your ticket as soon as possible.')

@bot.tree.command(name="toggle-gta-killing",description="toggle whether to kill gta tickets")
async def slash_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, id=moderator_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        global kill_gta_tickets
        kill_gta_tickets = not kill_gta_tickets
        update_status()
        print("Updated gta killing - " + str(kill_gta_tickets))
        await interaction.response.send_message("Updated gta killing - " + str(kill_gta_tickets))
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)
    
@bot.tree.command(name="toggle-rdr-killing",description="toggle whether to kill rdr tickets")
async def slash_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, id=moderator_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        global kill_rdr_tickets
        kill_rdr_tickets = not kill_rdr_tickets
        update_status()
        print("Updated rdr killing - " + str(kill_rdr_tickets))
        await interaction.response.send_message("Updated rdr killing - " + str(kill_rdr_tickets))
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.tree.command(name="toggle-cs2-killing",description="toggle whether to kill cs2 tickets")
async def slash_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, id=moderator_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        global kill_cs2_tickets
        kill_cs2_tickets = not kill_cs2_tickets
        update_status()
        print("Updated cs2 killing - " + str(kill_cs2_tickets))
        await interaction.response.send_message("Updated cs2 killing - " + str(kill_cs2_tickets))
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.tree.command(name="killing-status",description="get the status of the ticket killing")
async def slash_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, id=staff_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(":green_circle: = killing enabled, :red_circle: = killing disabled"
                                                "\nGTA: " + (":green_circle:" if kill_gta_tickets else ":red_circle:") +
                                                "\nRDR: " + (":green_circle:" if kill_rdr_tickets else ":red_circle:") +
                                                "\nCS2: " + (":green_circle:" if kill_cs2_tickets else ":red_circle:"))
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'We have logged in as {bot.user}')


def update_status():
    global kill_gta_tickets
    global kill_rdr_tickets
    global kill_cs2_tickets
    with open("last_state.txt", "w") as f:
        f.write(str(kill_gta_tickets) + "\n" + str(kill_rdr_tickets) + "\n" + str(kill_cs2_tickets))


bot.run(DISCORD_TOKEN)
