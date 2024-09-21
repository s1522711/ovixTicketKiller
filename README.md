# Ovix ticket killer
small and shitty discord.py bot made for ovix to auto delete tickets if they are created for a disabled game or delete password reset tickets that were not created for password resets  
  
also because i didnt want to create another bot for the minecraft server this bot also has minecraft server related commands (applications with crafty and comfywhitelist integration, granting staff role using crafty and luckperms and restarting, stopping and starting the server using crafty)

# Dependencies
this bot depends on:
- discord.py
- python-dotenv  
- aiohttp
before you can start the bot you will need to install its dependencies using the command bellow:  
```
pip install -U discord.py python-dotenv aiohttp
```

# Setup
in order for this bot to run you need to create a file called `.env` in the same directory as the .py file  
its contents will be formatted like this (replace the CAPS text):
```env
TOKEN="BOT TOKEN HERE"
TICKET_BOT_ID=TICKETTOOL USER ID HERE
MODERATOR_ROLE_ID=MODERATOR ROLE ID HERE
STAFF_ROLE_ID=NORMAL STAFF ROLE ID HERE
TRIAL_STAFF_ROLE_ID=TRIAL STAFF ROLE ID HERE
MINECRAFT_APPLICATIONS_CHANNEL_ID=CHANNEL ID FOR MINECRAFT APPLICATIONS HERE
MINECRAFT_ROLE_ID=ROLE ID FOR MINECRAFT CHANNEL ACCESS HERE
CRAFTY_BASE_URL="CRAFTY BASE URL HERE"
CRAFTY_API_USERNAME="API USERNAME HERE"
CRAFTY_API_PASSWORD="API PASSWORD HERE"
CRAFTY_SERVER_ID=SERVER ID HERE
MINECRAFT_SERVER_IP="MINECRAFT SERVER IP HERE"
UNVERIFIED_ROLE_ID=UNVERIFIED ROLE ID HERE
VERIFICATION_CHANNEL_ID=VERIFICATION CHANNEL ID HERE
LAST_STATUS_MESSAGE_CHANNEL_ID=SATUS MESSAGE CHANNEL ID HERE
```
after that you can run the bot via these commands:  
### on windows:
```
py main.py
```
### on linux:
```bash
python3 main.py
```
