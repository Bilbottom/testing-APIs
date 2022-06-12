import sys
import slack


if len(sys.argv) == 1:
    post_text = 'There was an error retrieving the latest task details.'
else:
    post_text = sys.argv[1]

OAuth = ''
client = slack.WebClient(token=OAuth)

client.chat_postMessage(
    channel='#bill-current-work',
    text=post_text
)
