import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import requests

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
        data = { "username": crafty_api_username, "password": crafty_api_password }
        response = requests.post(crafty_base_url + "auth/login", json=data)
        if response.status_code == 200:
            token = response.json()["data"]["token"]
            headers = { "Authorization": f"Bearer {token}", 'Content-Type': 'text/plain; charset=utf-8' }
            data = "comfywl add " + self.embed.fields[0].value.split("`")[1]
            response = requests.post(f"{crafty_base_url}servers/{crafty_server_id}/stdin", data=data, headers=headers)
            #response = requests.get(url + "servers", headers=headers)
            if response.status_code == 200:
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

        # Add the user to the whitelist
        data = { "username": crafty_api_username, "password": crafty_api_password }
        response = requests.post(crafty_base_url + "auth/login", json=data)
        if response.status_code == 200:
            token = response.json()["data"]["token"]
            headers = { "Authorization": f"Bearer {token}", 'Content-Type': 'text/plain; charset=utf-8' }
            data = "comfywl remove " + self.embed.fields[0].value.split("`")[1]
            response = requests.post(f"{crafty_base_url}servers/{crafty_server_id}/stdin", data=data, headers=headers)
            if response.status_code == 200:
                print(f"Removed {self.embed.fields[0].value} from the whitelist")
            else:
                print(f"Failed to remove {self.embed.fields[0].value} from the whitelist")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}!')

@bot.tree.command(name="mc-apply", description="Apply for access to the Minecraft server")
async def slash_command(interaction: discord.Interaction, username: str):
    role = discord.utils.get(interaction.guild.roles, id=unverified_role_id)
    if role in interaction.user.roles:
        await interaction.response.send_message(f"You must verify your account to apply for the Minecraft server. Please check your DMs for instructions on how to verify your account.\nTo verify your account, please type `/verify` in the <#{verification_channel_id}> channel.", ephemeral=True)
        return
    channel = bot.get_channel(minecraft_applications_channel_id)
    embedVar = discord.Embed(title="Minecraft Application - Pending", description=f"{interaction.user.mention} created an application", color=0x000000)
    embedVar.add_field(name="Minecraft Username: ", value=f"`{username}`", inline=False)
    view = ApplicationView(interaction.user, embedVar)
    await channel.send(embed=embedVar, view=view)
    await interaction.response.send_message("Your application has been submitted. You will be notified if you are accepted or denied.\nMake sure to check if you have DMs enabled from server members.", ephemeral=True)

@bot.tree.command(name="get-staff", description="Get staff rank in server (staff only)")
async def slash_command(interaction: discord.Interaction, username: str):
    role = discord.utils.get(interaction.guild.roles, id=staff_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        # Add the user to the whitelist
        data = {"username": crafty_api_username, "password": crafty_api_password}
        response = requests.post(crafty_base_url + "auth/login", json=data)
        if response.status_code == 200:
            token = response.json()["data"]["token"]
            headers = {"Authorization": f"Bearer {token}", 'Content-Type': 'text/plain; charset=utf-8'}
            data = f"lp user {username} parent add admin"
            response = requests.post(f"{crafty_base_url}servers/{crafty_server_id}/stdin", data=data, headers=headers)
            if response.status_code == 200:
                print(f"Awarded staff rank to {username}")
                await interaction.response.send_message(f"Awarded staff rank to {username}")
            else:
                print(f"Failed to award staff rank to {username}")
                await interaction.response.send_message(f"Failed to award staff rank to {username}")
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.tree.command(name="remove-staff", description="Remove staff rank in server (staff only)")
async def slash_command(interaction: discord.Interaction, username: str):
    role = discord.utils.get(interaction.guild.roles, id=staff_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        # Add the user to the whitelist
        data = {"username": crafty_api_username, "password": crafty_api_password}
        response = requests.post(crafty_base_url + "auth/login", json=data)
        if response.status_code == 200:
            token = response.json()["data"]["token"]
            headers = {"Authorization": f"Bearer {token}", 'Content-Type': 'text/plain; charset=utf-8'}
            data = f"lp user {username} parent remove admin"
            response = requests.post(f"{crafty_base_url}servers/{crafty_server_id}/stdin", data=data, headers=headers)
            if response.status_code == 200:
                print(f"Removed staff rank from {username}")
                await interaction.response.send_message(f"Removed staff rank from {username}")
            else:
                print(f"Failed to remove staff rank from {username}")
                await interaction.response.send_message(f"Failed to remove staff rank from {username}")
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)

@bot.tree.command(name="restart-server", description="Restart the Minecraft server (staff only)")
async def slash_command(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, id=staff_role_id)
    if role in interaction.user.roles or interaction.user.guild_permissions.administrator:
        # Add the user to the whitelist
        data = {"username": crafty_api_username, "password": crafty_api_password}
        response = requests.post(crafty_base_url + "auth/login", json=data)
        if response.status_code == 200:
            token = response.json()["data"]["token"]
            headers = {"Authorization": f"Bearer {token}", 'Content-Type': 'text/plain; charset=utf-8'}
            data = "restart"
            response = requests.post(f"{crafty_base_url}servers/{crafty_server_id}/action/restart_server", data=data, headers=headers)
            if response.status_code == 200:
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
        # Add the user to the whitelist
        data = {"username": crafty_api_username, "password": crafty_api_password}
        response = requests.post(crafty_base_url + "auth/login", json=data)
        if response.status_code == 200:
            token = response.json()["data"]["token"]
            headers = {"Authorization": f"Bearer {token}", 'Content-Type': 'text/plain; charset=utf-8'}
            data = "restart"
            response = requests.post(f"{crafty_base_url}servers/{crafty_server_id}/action/stop_server", data=data, headers=headers)
            if response.status_code == 200:
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
        # Add the user to the whitelist
        data = {"username": crafty_api_username, "password": crafty_api_password}
        response = requests.post(crafty_base_url + "auth/login", json=data)
        if response.status_code == 200:
            token = response.json()["data"]["token"]
            headers = {"Authorization": f"Bearer {token}", 'Content-Type': 'text/plain; charset=utf-8'}
            data = "restart"
            response = requests.post(f"{crafty_base_url}servers/{crafty_server_id}/action/start_server", data=data, headers=headers)
            if response.status_code == 200:
                print("Started the server")
                await interaction.response.send_message("Started the server")
            else:
                print("Failed to start the server")
                await interaction.response.send_message("Failed to start the server")
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
