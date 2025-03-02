import sys
import os

import dotenv
import slack  # pip install slack_sdk


if __name__ == "__main__":
    post_text = "Example text"
elif len(sys.argv) == 1:
    # minimum is 1 arg, namely the script
    post_text = "There was an error retrieving the message"
else:
    post_text = sys.argv[1]


user_me = "U01K959PA8Y"
dotenv.load_dotenv()
client = slack.WebClient(token=os.environ["SLACK_TOKEN"])


client.chat_postMessage(channel="#bills-bot", text=post_text)
