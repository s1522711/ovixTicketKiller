from copyreg import constructor

import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import aiohttp
import enum

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
minecraft_applications_channel_id = int(os.getenv("MINECRAFT_APPLICATIONS_CHANNEL_ID"))
print("minecraft applications channel id: " + str(minecraft_applications_channel_id))
minecraft_role_id = int(os.getenv("MINECRAFT_ROLE_ID"))
print("minecraft role id: " + str(minecraft_role_id))
crafty_base_url = os.getenv("CRAFTY_BASE_URL") + "/api/v2/"
print("crafty base url: " + crafty_base_url)
crafty_api_username = os.getenv("CRAFTY_API_USERNAME")
print("crafty api username: " + crafty_api_username)
crafty_api_password = os.getenv("CRAFTY_API_PASSWORD")
print("crafty api password: " + crafty_api_password)
crafty_server_id = os.getenv("CRAFTY_SERVER_ID")
print("crafty server id: " + crafty_server_id)
minecraft_server_ip = os.getenv("MINECRAFT_SERVER_IP")
print("minecraft server ip: " + minecraft_server_ip)
unverified_role_id = int(os.getenv("UNVERIFIED_ROLE_ID"))
print("unverified role id: " + str(unverified_role_id))
verification_channel_id = int(os.getenv("VERIFICATION_CHANNEL_ID"))
print("verification channel id: " + str(verification_channel_id))
last_status_message_channel_id = int(os.getenv("LAST_STATUS_MESSAGE_CHANNEL_ID"))
print("last status message channel id: " + str(last_status_message_channel_id))
retard_channel_id = int(os.getenv("RETARD_CHANNEL_ID"))
print("retard_channel_id:", retard_channel_id)
ticket_category_ids = os.getenv("TICKET_CATEGORY_IDS").replace(" ", "").split(",")
ticket_category_ids = [eval(i) for i in ticket_category_ids]
print("ticket_category_id's:", ticket_category_ids)


kill_gta_tickets = False
kill_rdr_tickets = False
kill_cs2_tickets = False
kill_unverified_tickets = False

# 0 = down, 1 = up, 2 = updating
status_api = 1
status_rdr2 = 1
status_gta = 1
status_cs2 = 1
DOWN_EMOJI = ":red_circle:"
UP_EMOJI = ":green_circle:"
UPDATING_EMOJI = ":yellow_circle:"
last_status_message = None
last_status_message_id = 000000000

async def update_last_state():
    global last_status_message
    global kill_gta_tickets
    global kill_rdr_tickets
    global kill_cs2_tickets
    global kill_unverified_tickets
    global status_api
    global status_rdr2
    global status_gta
    global status_cs2
    with open("last_state.txt", "w") as f:
        f.write(str(kill_gta_tickets) + "\n" + str(kill_rdr_tickets) + "\n" + str(kill_cs2_tickets) + "\n" + str(kill_unverified_tickets) + "\n")
        f.write("----------------\n")
        f.write(str(status_api) + "\n" + str(status_rdr2) + "\n" + str(status_gta) + "\n" + str(status_cs2) + "\n")
        f.write(str(last_status_message.id) + "\n")

try:
    with open("last_state.txt", "r") as f:
        kill_gta_tickets = f.readline().strip() == "True"
        kill_rdr_tickets = f.readline().strip() == "True"
        kill_cs2_tickets = f.readline().strip() == "True"
        kill_unverified_tickets = f.readline().strip() == "True"
        f.readline()
        status_api = int(f.readline().strip())
        status_rdr2 = int(f.readline().strip())
        status_gta = int(f.readline().strip())
        status_cs2 = int(f.readline().strip())
        last_status_message_id = f.readline().strip()
except FileNotFoundError:
    print("last_state.txt not found, using defaults")
    with open("last_state.txt", "w") as f:
        f.write(str(kill_gta_tickets) + "\n" + str(kill_rdr_tickets) + "\n" + str(kill_cs2_tickets) + "\n" + str(kill_unverified_tickets) + "\n")
        f.write("----------------\n")
        f.write(str(status_api) + "\n" + str(status_rdr2) + "\n" + str(status_gta) + "\n" + str(status_cs2) + "\n")
        f.write(str(last_status_message_id) + "\n")

print(kill_gta_tickets, kill_rdr_tickets, kill_cs2_tickets, kill_unverified_tickets)
print(status_api, status_rdr2, status_gta, status_cs2)
print(last_status_message_id)


async def update_status_message():
    global last_status_message
    global last_status_message_id
    global last_status_message_channel_id
    global status_api
    global status_rdr2
    global status_gta
    global status_cs2
    # build the embed
    embed1_description = f"**{UP_EMOJI} | Online**\n**{UPDATING_EMOJI} | Updating**\n**{DOWN_EMOJI} | Offline**"
    embed1 = discord.Embed(title="Status Guide", color=discord.Color.dark_gray(), description=embed1_description)
    embed2_api_line = f"API: {UP_EMOJI if status_api == 1 else DOWN_EMOJI if status_api == 0 else UPDATING_EMOJI}"
    embed2_rdr2_line = f"Read Dead Redemption 2: {UP_EMOJI if status_rdr2 == 1 else DOWN_EMOJI if status_rdr2 == 0 else UPDATING_EMOJI}"
    embed2_gta_line = f"Grand Theft Auto 5: {UP_EMOJI if status_gta == 1 else DOWN_EMOJI if status_gta == 0 else UPDATING_EMOJI}"
    embed2_cs2_line = f"Counter-Strike 2: {UP_EMOJI if status_cs2 == 1 else DOWN_EMOJI if status_cs2 == 0 else UPDATING_EMOJI}"
    embed2_description = f"{embed2_api_line}\n{embed2_rdr2_line}\n{embed2_gta_line}\n{embed2_cs2_line}"
    embed2 = discord.Embed(title="Product Status", color=discord.Color.dark_gray(), description=embed2_description)
    embed3_description_gtakill = f"Grand Theft Auto 5 Tickets: {UP_EMOJI if not kill_gta_tickets else DOWN_EMOJI}"
    embed3_description_rdrkill = f"Red Dead Redemption 2 Tickets: {UP_EMOJI if not kill_rdr_tickets else DOWN_EMOJI}"
    embed3_description_cs2kill = f"Counter-Strike 2 Tickets: {UP_EMOJI if not kill_cs2_tickets else DOWN_EMOJI}"
    embed3_description_unverifiedkill = f"Unverified Password Reset Tickets: {UP_EMOJI if not kill_unverified_tickets else DOWN_EMOJI}"
    embed3_description = f"{embed3_description_gtakill}\n{embed3_description_rdrkill}\n{embed3_description_cs2kill}\n{embed3_description_unverifiedkill}"
    embed3 = discord.Embed(title="Ticket Status", color=discord.Color.dark_gray(), description=embed3_description)
    # send the message
    if last_status_message_id != 000000000 and last_status_message_channel_id is not None:
        channel = bot.get_channel(int(last_status_message_channel_id))
        if channel is not None:
            try:
                last_status_message = await channel.fetch_message(int(last_status_message_id))
            except discord.errors.NotFound:
                print("last status message not found")
                last_status_message = None
    if last_status_message is not None:
        await asyncio.create_task(last_status_message.edit(embeds=[embed1, embed2, embed3]))
    else:
        print("last status message is None")
        channel = bot.get_channel(int(last_status_message_channel_id))
        if channel is not None:
            last_status_message = await channel.send(embeds=[embed1, embed2, embed3])
            last_status_message_id = last_status_message.id
            last_status_message_channel_id = last_status_message.channel.id
            await update_last_state()

@bot.event
async def on_message(message):
    global kill_gta_tickets
    global kill_rdr_tickets
    global kill_cs2_tickets
    global kill_unverified_tickets

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
        if kill_unverified_tickets:
            print("found unverified password reset ticket")
            await message.channel.send('Hello! the unverified password reset category has been disabled!')
            await message.channel.send('this ticket will be closed in 5 seconds')
            await asyncio.sleep(1)
            for i in range(4):
                await message.channel.send(str(4-i))
                await asyncio.sleep(1)
            await message.channel.send('0 - goodbye!')
            await asyncio.sleep(1)
            await message.channel.send('$close BOT: UNVERIFIED PASSWORD RESET CATEGORY DISABLED')
            await asyncio.sleep(0.5)
            await message.channel.send('$transcript')
            await asyncio.sleep(0.5)
            await message.channel.send('$delete')
            return
        elif 'ye' not in message.content.split('//')[2].lower():
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

    if message.author.id == ticket_bot_id and '//' in message.content and 'pswrd' not in message.content.split('//')[1].lower():
        # the opening reason is in the embed field called "Why are you creating this ticket?"
        opening_reason = message.embeds[1].description.split('\n')[1].replace('`', '')
        read_status = message.embeds[1].description.split('\n')[7].replace('`', '')
        ticket_game = message.content.split('//')[1]
        print(f"ticket opened with the reason: {opening_reason} and read status: {read_status} for the game: {ticket_game}")
        await message.channel.send('||<@&' + str(staff_role_id) + '> <@&' + str(trial_staff_role_id) + '>||'
                                   f'\nGame: {ticket_game}, read? {read_status}, reason: {opening_reason}'
                                   '\nPlease do not ping staff, we will get to your ticket as soon as possible.')

    if message.author.id == ticket_bot_id and '//' in message.content and 'pswrd' in message.content.split('//')[1].lower():
        opening_reason = message.embeds[1].description.split('\n')[1].replace('`', '')
        print(f"unverified ticket opened with the reason: {opening_reason}")
        await message.channel.send('||<@&' + str(staff_role_id) + '> <@&' + str(trial_staff_role_id) + '>||'
                                   f'\nType: unverified, reason: {opening_reason}'
                                   '\nPlease do not ping staff, we will get to your ticket as soon as possible.')

    # check if the message is in one of the ticket channel categories
    try:
        if message.channel.category_id in ticket_category_ids:
            message_author = message.author
            if message_author is not None:
                if message_author.bot:
                    return
                if message_author.guild_permissions.administrator:
                    return
                role = discord.utils.get(message.guild.roles, id=staff_role_id)
                if role in message_author.roles:
                    return
                role = discord.utils.get(message.guild.roles, id=trial_staff_role_id)
                if role in message_author.roles:
                    return
                if not message.mentions:
                    return
                if message.reference: # if the message is a reply
                    return
                # if there are mentions in the message, send a warning to the retard channel
                print(f"ping detected in channel id: {message.channel.id} by user id: {message_author.mention}")
                retard_channel = bot.get_channel(retard_channel_id)
                await retard_channel.send(f"{message_author.mention} has pinged someone in <#{message.channel.id}>")
                # warn the user
                for x in range(5):
                    await message.channel.send(f"Please dont ping staff! {message_author.mention}")
                await message.channel.send("hope you understand :)")
    except AttributeError:
        pass

"""
@bot.tree.command(name="toggle-gta-killing",description="toggle whether to kill gta tickets")
async def slash_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, id=moderator_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        global kill_gta_tickets
        kill_gta_tickets = not kill_gta_tickets
        await update_last_state()
        await update_status_message()
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
        await update_last_state()
        await update_status_message()
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
        await update_last_state()
        await update_status_message()
        print("Updated cs2 killing - " + str(kill_cs2_tickets))
        await interaction.response.send_message("Updated cs2 killing - " + str(kill_cs2_tickets))
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)
        
@bot.tree.command(name="toggle-unverified-killing",description="toggle whether to kill unverified tickets")
async def slash_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, id=moderator_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        global kill_unverified_tickets
        kill_unverified_tickets = not kill_unverified_tickets
        await update_last_state()
        await update_status_message()
        print("Updated unverified killing - " + str(kill_unverified_tickets))
        await interaction.response.send_message("Updated unverified killing - " + str(kill_unverified_tickets))
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)
"""


class KillingOptions(enum.IntEnum):
    KILL = 1
    UNKILL = 0


class KillingTicketOptions(enum.Enum):
    GTA = 1
    RDR = 2
    CS2 = 3
    UNVERIFIED = 4

@bot.tree.command(name="set-killing",description="set the killing status of a ticket category")
@app_commands.describe(option="1 = kill, 0 = unkill", ticket_option="1 = GTA, 2 = RDR, 3 = CS2, 4 = unverified")
async def slash_command(interaction: discord.Interaction, option: KillingOptions, ticket_option: KillingTicketOptions):
    role = discord.utils.get(interaction.guild.roles, id=moderator_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        global kill_gta_tickets
        global kill_rdr_tickets
        global kill_cs2_tickets
        global kill_unverified_tickets
        if ticket_option == KillingTicketOptions.GTA:
            kill_gta_tickets = option == KillingOptions.KILL
        elif ticket_option == KillingTicketOptions.RDR:
            kill_rdr_tickets = option == KillingOptions.KILL
        elif ticket_option == KillingTicketOptions.CS2:
            kill_cs2_tickets = option == KillingOptions.KILL
        elif ticket_option == KillingTicketOptions.UNVERIFIED:
            kill_unverified_tickets = option == KillingOptions.KILL
        await update_last_state()
        await update_status_message()
        print(f"Updated killing of {ticket_option.name} to {option.name}")
        await interaction.response.send_message(f"Updated killing of {ticket_option.name} to {option.name}")
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.tree.command(name="killing-status",description="get the status of the ticket killing")
async def slash_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, id=staff_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(":green_circle: = killing enabled, :red_circle: = killing disabled"
                                                "\nGTA: " + (":green_circle:" if kill_gta_tickets else ":red_circle:") +
                                                "\nRDR: " + (":green_circle:" if kill_rdr_tickets else ":red_circle:") +
                                                "\nCS2: " + (":green_circle:" if kill_cs2_tickets else ":red_circle:") +
                                                "\nUnverified: " + (":green_circle:" if kill_unverified_tickets else ":red_circle:"))
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)


class ApplicationView(discord.ui.View):
    def __init__(self, user, embed):
        super().__init__(timeout=None)
        self.user = user
        self.embed = embed

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success)
    async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.color = discord.Color.green()
        self.embed.title = "Minecraft Application - Accepted"
        await interaction.response.edit_message(embed=self.embed)
        embed_description = self.embed.description
        user_id = embed_description.split("  created an application")[0]
        user_id = user_id.split("@")[1]
        user_id = user_id.split(">")[0]
        # Get the guild member
        guild = interaction.guild
        member = guild.get_member(int(user_id))

        if member is None:
            member = await guild.fetch_member(int(user_id))

        # Send the DM to the user
        embedVar = discord.Embed(
            title="Minecraft Application",
            description=f"Your application has been accepted {member.mention}!",
            color=discord.Color.green()
        )
        embedVar.add_field(name="The Minecraft username that was whitelisted: ", value=self.embed.fields[0].value,
                           inline=False)
        embedVar.add_field(name="You can now join the server at: ", value=f"`{minecraft_server_ip}`", inline=False)
        embedVar.add_field(name="Minecraft Version: ", value="`1.21`", inline=False)
        await member.send(embed=embedVar)

        # Add the role to the member
        role = guild.get_role(minecraft_role_id)
        if role is not None:
            await member.add_roles(role)
        else:
            print(f"Role with ID {minecraft_role_id} not found")

        # Add the user to the whitelist
        async with aiohttp.ClientSession() as session:
            data = {"username": crafty_api_username, "password": crafty_api_password}
            async with session.post(crafty_base_url + "auth/login", json=data) as response:
                if response.status == 200:
                    token = (await response.json())["data"]["token"]
                    headers = {"Authorization": f"Bearer {token}", 'Content-Type': 'text/plain; charset=utf-8'}
                    data = "comfywl add " + self.embed.fields[0].value.split("`")[1]
                    async with session.post(f"{crafty_base_url}servers/{crafty_server_id}/stdin", data=data, headers=headers) as response:
                        if response.status == 200:
                            print(f"Added {self.embed.fields[0].value} to the whitelist")
                        else:
                            print(f"Failed to add {self.embed.fields[0].value} to the whitelist")

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger)
    async def deny_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.color = discord.Color.red()
        self.embed.title = "Minecraft Application - Denied"
        await interaction.response.edit_message(embed=self.embed)

        # Extract the user ID from the embed description
        embed_description = self.embed.description
        user_id = embed_description.split("  created an application")[0]
        user_id = user_id.split("@")[1]
        user_id = user_id.split(">")[0]

        # Get the guild member
        guild = interaction.guild
        member = guild.get_member(int(user_id))

        if member is None:
            member = await guild.fetch_member(int(user_id))

        # Send the denial DM to the member
        try:
            await member.send(f"We are sorry to announce that your application has been denied {member.mention}!")
            await member.send("If you have any questions, feel free to ask in the server.")
        except discord.Forbidden:
            print(f"Could not send DM to {member} (ID: {member.id}).")

        role = guild.get_role(minecraft_role_id)
        if role:
            await member.remove_roles(role)

        # Remove the user from the whitelist
        async with aiohttp.ClientSession() as session:
            data = {"username": crafty_api_username, "password": crafty_api_password}
            async with session.post(crafty_base_url + "auth/login", json=data) as response:
                if response.status == 200:
                    token = (await response.json())["data"]["token"]
                    headers = {"Authorization": f"Bearer {token}", 'Content-Type': 'text/plain; charset=utf-8'}
                    data = "comfywl remove " + self.embed.fields[0].value.split("`")[1]
                    async with session.post(f"{crafty_base_url}servers/{crafty_server_id}/stdin", data=data, headers=headers) as response:
                        if response.status == 200:
                            print(f"Removed {self.embed.fields[0].value} from the whitelist")
                        else:
                            print(f"Failed to remove {self.embed.fields[0].value} from the whitelist")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}!')

@bot.tree.command(name="mc-apply", description="Apply for access to the Minecraft server")
@app_commands.describe(username="Minecraft username")
@app_commands.rename(username="minecraft-username")
async def slash_command(interaction: discord.Interaction, username: str):
    role = discord.utils.get(interaction.guild.roles, id=unverified_role_id)
    if role in interaction.user.roles:
        await interaction.response.send_message(f"You must verify your account to apply for the Minecraft server. Please read the line below for instructions on how to verify your account.\nTo verify your account, please type `/verify` in the <#{verification_channel_id}> channel.", ephemeral=True)
        return
    channel = bot.get_channel(minecraft_applications_channel_id)
    embedVar = discord.Embed(title="Minecraft Application - Pending", description=f"{interaction.user.mention} created an application", color=0x000000)
    embedVar.add_field(name="Minecraft Username: ", value=f"`{username}`", inline=False)
    view = ApplicationView(interaction.user, embedVar)
    await channel.send(embed=embedVar, view=view)
    await interaction.response.send_message("Your application has been submitted. You will be notified if you are accepted or denied.\nMake sure to check if you have DMs enabled from server members.", ephemeral=True)
    
@bot.tree.command(name="mc-apply-other", description="Create an application for a different user (admin only)")
@app_commands.describe(username="Select a user", minecraft_username="Minecraft username")
@app_commands.rename(username="user", minecraft_username="minecraft-username")
async def slash_command(interaction: discord.Interaction, username: discord.User, minecraft_username: str):
    role = discord.utils.get(interaction.guild.roles, id=staff_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        channel = bot.get_channel(minecraft_applications_channel_id)
        embedVar = discord.Embed(title="Minecraft Application - Pending", description=f"{username.mention} created an application", color=0x000000)
        embedVar.add_field(name="Minecraft Username: ", value=f"`{minecraft_username}`", inline=False)
        view = ApplicationView(interaction.user, embedVar)
        await channel.send(embed=embedVar, view=view)
        await interaction.response.send_message(f"Application for {username.mention} has been submitted. They will be notified if they are accepted or denied.", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.tree.command(name="get-staff", description="Get staff rank in server (staff only)")
@app_commands.describe(username="Minecraft username")
@app_commands.rename(username="minecraft-username")
async def slash_command(interaction: discord.Interaction, username: str):
    role = discord.utils.get(interaction.guild.roles, id=staff_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        async with aiohttp.ClientSession() as session:
            data = {"username": crafty_api_username, "password": crafty_api_password}
            async with session.post(crafty_base_url + "auth/login", json=data) as response:
                if response.status == 200:
                    token = (await response.json())["data"]["token"]
                    headers = {"Authorization": f"Bearer {token}", 'Content-Type': 'text/plain; charset=utf-8'}
                    data = f"lp user {username} parent add admin"
                    async with session.post(f"{crafty_base_url}servers/{crafty_server_id}/stdin", data=data, headers=headers) as response:
                        if response.status == 200:
                            data = f"op {username}"
                            async with session.post(f"{crafty_base_url}servers/{crafty_server_id}/stdin", data=data, headers=headers) as response:
                                if response.status == 200:
                                    print(f"Awarded staff rank to {username}")
                                    await interaction.response.send_message(f"Awarded staff rank to {username}")
                                else:
                                    print(f"Failed to award staff rank to {username}")
                                    await interaction.response.send_message(f"Failed to award staff rank to {username}")
                        else:
                            print(f"Failed to award staff rank to {username}")
                            await interaction.response.send_message(f"Failed to award staff rank to {username}")
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.tree.command(name="remove-staff", description="Remove staff rank in server (staff only)")
@app_commands.describe(username="Minecraft username")
@app_commands.rename(username="minecraft-username")
async def slash_command(interaction: discord.Interaction, username: str):
    role = discord.utils.get(interaction.guild.roles, id=staff_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        async with aiohttp.ClientSession() as session:
            data = {"username": crafty_api_username, "password": crafty_api_password}
            async with session.post(crafty_base_url + "auth/login", json=data) as response:
                if response.status == 200:
                    token = (await response.json())["data"]["token"]
                    headers = {"Authorization": f"Bearer {token}", 'Content-Type': 'text/plain; charset=utf-8'}
                    data = f"lp user {username} parent remove admin"
                    async with session.post(f"{crafty_base_url}servers/{crafty_server_id}/stdin", data=data, headers=headers) as response:
                        if response.status == 200:
                            data = f"deop {username}"
                            async with session.post(f"{crafty_base_url}servers/{crafty_server_id}/stdin", data=data, headers=headers) as response:
                                if response.status == 200:
                                    print(f"Removed staff rank from {username}")
                                    await interaction.response.send_message(f"Removed staff rank from {username}")
                                else:
                                    print(f"Failed to remove staff rank from {username}")
                                    await interaction.response.send_message(f"Failed to remove staff rank from {username}")
                        else:
                            print(f"Failed to remove staff rank from {username}")
                            await interaction.response.send_message(f"Failed to remove staff rank from {username}")
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.tree.command(name="restart-server", description="Restart the Minecraft server (staff only)")
async def slash_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, id=staff_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        async with aiohttp.ClientSession() as session:
            data = {"username": crafty_api_username, "password": crafty_api_password}
            async with session.post(crafty_base_url + "auth/login", json=data) as response:
                if response.status == 200:
                    token = (await response.json())["data"]["token"]
                    headers = {"Authorization": f"Bearer {token}", 'Content-Type': 'text/plain; charset=utf-8'}
                    data = "restart"
                    async with session.post(f"{crafty_base_url}servers/{crafty_server_id}/action/restart_server", data=data, headers=headers) as response:
                        if response.status == 200:
                            print("Restarted the server")
                            await interaction.response.send_message("Restarted the server")
                        else:
                            print("Failed to restart the server")
                            await interaction.response.send_message("Failed to restart the server")
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.tree.command(name="stop-server", description="Stop the Minecraft server (staff only)")
async def slash_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, id=staff_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        async with aiohttp.ClientSession() as session:
            data = {"username": crafty_api_username, "password": crafty_api_password}
            async with session.post(crafty_base_url + "auth/login", json=data) as response:
                if response.status == 200:
                    token = (await response.json())["data"]["token"]
                    headers = {"Authorization": f"Bearer {token}", 'Content-Type': 'text/plain; charset=utf-8'}
                    data = "restart"
                    async with session.post(f"{crafty_base_url}servers/{crafty_server_id}/action/stop_server", data=data, headers=headers) as response:
                        if response.status == 200:
                            print("Stopped the server")
                            await interaction.response.send_message("Stopped the server")
                        else:
                            print("Failed to stop the server")
                            await interaction.response.send_message("Failed to stop the server")
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.tree.command(name="start-server", description="start the Minecraft server (staff only)")
async def slash_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, id=staff_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        async with aiohttp.ClientSession() as session:
            data = {"username": crafty_api_username, "password": crafty_api_password}
            async with session.post(crafty_base_url + "auth/login", json=data) as response:
                if response.status == 200:
                    token = (await response.json())["data"]["token"]
                    headers = {"Authorization": f"Bearer {token}", 'Content-Type': 'text/plain; charset=utf-8'}
                    data = "restart"
                    async with session.post(f"{crafty_base_url}servers/{crafty_server_id}/action/start_server", data=data, headers=headers) as response:
                        if response.status == 200:
                            print("Started the server")
                            await interaction.response.send_message("Started the server")
                        else:
                            print("Failed to start the server")
                            await interaction.response.send_message("Failed to start the server")
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)


class Status(enum.IntEnum):
    UP = 1
    DOWN = 0
    UPDATING = 2
"""
@bot.tree.command(name="set-status-api", description="Set the status of the API")
@app_commands.describe(status="0 = down, 1 = up, 2 = updating")
async def slash_command(interaction: discord.Interaction, status: Status):
    role = discord.utils.get(interaction.guild.roles, id=staff_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        global status_api
        status_api = status
        await update_status_message()
        await update_last_state()
        await interaction.response.send_message("Updated the API status")
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.tree.command(name="set-status-rdr2", description="Set the status of Red Dead Redemption 2")
@app_commands.describe(status="0 = down, 1 = up, 2 = updating")
async def slash_command(interaction: discord.Interaction, status: Status):
    role = discord.utils.get(interaction.guild.roles, id=staff_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        global status_rdr2
        status_rdr2 = status
        await update_status_message()
        await update_last_state()
        await interaction.response.send_message("Updated the Red Dead Redemption 2 status")
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.tree.command(name="set-status-gta", description="Set the status of Grand Theft Auto 5")
@app_commands.describe(status="0 = down, 1 = up, 2 = updating")
async def slash_command(interaction: discord.Interaction, status: Status):
    role = discord.utils.get(interaction.guild.roles, id=staff_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        global status_gta
        status_gta = status
        await update_status_message()
        await update_last_state()
        await interaction.response.send_message("Updated the Grand Theft Auto 5 status")
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.tree.command(name="set-status-cs2", description="Set the status of Counter-Strike 2")
@app_commands.describe(status="0 = down, 1 = up, 2 = updating")
async def slash_command(interaction: discord.Interaction, status: Status):
    role = discord.utils.get(interaction.guild.roles, id=staff_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        global status_cs2
        status_cs2 = status
        await update_status_message()
        await update_last_state()
        await interaction.response.send_message("Updated the Counter-Strike 2 status")
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)
"""


class StatusOptions(enum.Enum):
    API = 1
    RDR2 = 2
    GTA = 3
    CS2 = 4

@bot.tree.command(name="set-product-status", description="Set the status of the products")
@app_commands.describe(status="0 = down, 1 = up, 2 = updating", product="API = 1, Red Dead Redemption 2 = 2, Grand Theft Auto 5 = 3, Counter-Strike 2 = 4")
async def slash_command(interaction: discord.Interaction, status: Status, product: StatusOptions):
    role = discord.utils.get(interaction.guild.roles, id=staff_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        status = int(status)
        if product == StatusOptions.API:
            global status_api
            status_api = status
        elif product == StatusOptions.RDR2:
            global status_rdr2
            status_rdr2 = status
        elif product == StatusOptions.GTA:
            global status_gta
            status_gta = status
        elif product == StatusOptions.CS2:
            global status_cs2
            status_cs2 = status
        await update_status_message()
        await update_last_state()
        await interaction.response.send_message("Updated the product status")
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.tree.command(name="get-status", description="Get the status of the products")
async def slash_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, id=staff_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(":green_circle: = online, :red_circle: = offline, :yellow_circle: = updating"
                                                "\nAPI: " + (":green_circle:" if status_api == 1 else ":red_circle:" if status_api == 0 else ":yellow_circle:") +
                                                "\nRed Dead Redemption 2: " + (":green_circle:" if status_rdr2 == 1 else ":red_circle:" if status_rdr2 == 0 else ":yellow_circle:") +
                                                "\nGrand Theft Auto 5: " + (":green_circle:" if status_gta == 1 else ":red_circle:" if status_gta == 0 else ":yellow_circle:") +
                                                "\nCounter-Strike 2: " + (":green_circle:" if status_cs2 == 1 else ":red_circle:" if status_cs2 == 0 else ":yellow_circle:"))
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.tree.command(name="close-ticket", description="Close a ticket (staff only)")
async def slash_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, id=staff_role_id)
    if role in interaction.user.roles:
        closer = interaction.user
        await interaction.response.send_message('closing ticket in 5 seconds', ephemeral=True)
        print(f'closing ticket in 5 seconds by {closer} in {interaction.channel} in {interaction.channel.category}')
        await interaction.channel.send('Hello! this ticket will be closed in 5 seconds')
        await asyncio.sleep(1)
        for i in range(4):
            await interaction.channel.send(str(4-i))
            await asyncio.sleep(1)
        await interaction.channel.send('0 - goodbye!')
        await asyncio.sleep(1)
        await interaction.channel.send(f'$close Bot autoclose - {closer.mention}')
        await asyncio.sleep(0.5)
        await interaction.channel.send('$transcript')
        await asyncio.sleep(0.5)
        await interaction.channel.send('$delete')
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'We have logged in as {bot.user}')
    await update_status_message()


bot.run(DISCORD_TOKEN)
