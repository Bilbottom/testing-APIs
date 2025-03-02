import os

import dotenv
import slack  # pip install slack_sdk

dotenv.load_dotenv()


def main() -> None:
    user_me = "U01K959PA8Y"
    client = slack.WebClient(token=os.environ["SLACK_TOKEN"])

    # client.chat_postMessage(channel='#bills-bot', text='Hello, World!')
    client.users_setPresence(presence="away", user=user_me)

    print(client.users_getPresence(user=user_me))
    # print(client.users_info(user=user_me))
