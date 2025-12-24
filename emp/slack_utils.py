import os
from dotenv import load_dotenv

# 👇 Load environment variables from .env file
load_dotenv()

# 👇 Access them using os.getenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

print("Bot token:", SLACK_BOT_TOKEN)
print("Channel ID:", CHANNEL_ID)
