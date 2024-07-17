# Ovix ticket killer
small and shitty discord.py bot made for ovix to auto delete tickets if they are created for a disabled game

# Dependencies
this bot depends on:
- discord.py
- python-dotenv  
before you can start the bot you will need to install its dependencies using the command bellow:  
```
pip install -U discord.py python-dotenv
```

# Setup
in order for this bot to run you need to create a .env file in the same directory as the .py file  
its contents will be formatted like this (replace the CAPS text):
```env
TOKEN="BOT TOKEN HERE"
TICKET_BOT_ID=TICKETTOOL USER ID HERE
MODERATOR_ROLE_ID=MODERATOR ROLE ID HERE
STAFF_ROLE_ID=NORMAL STAFF ROLE ID HERE
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
