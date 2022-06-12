import slack
import os
from pathlib import Path
from dotenv import load_dotenv

user_me = 'U01K959PA8Y'

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

# client.chat_postMessage(channel='#bills-bot', text='Hello, World!')

client.users_setPresence(presence='away', user=user_me)

print(client.users_getPresence(user=user_me))
# print(client.users_info(user=user_me))
