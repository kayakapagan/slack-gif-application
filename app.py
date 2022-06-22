import os
import logging
import requests

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from dotenv import load_dotenv
load_dotenv()

SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
GIPHY_KEY = os.environ["GIPHY_KEY"]

app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET, name="Gif Finder")
logger = logging.getLogger(__name__)


@app.action("channel_selected")
def action_channel_selected(body, ack, say):
    # Acknowledge the action
    ack()
    say(channel=body["actions"][0]["selected_channel"], blocks=[{
            "type": "image",
            "title": {
                "type": "plain_text",
                "text": "Enjoy your gif"
            },
            "block_id": "image_selected",
            "alt_text": "selected image from Giphy.",
            "image_url": body["actions"][0]["block_id"],
        }])

@app.action("item_selected")
def action_item_selected(body, ack, say):
    # Acknowledge the action
    ack()
    blocks = [
        {
            "type": "section",
            "block_id": body["actions"][0]["selected_option"]["value"],
            "text": {
                "type": "mrkdwn",
                "text": "Pick a channel from the dropdown list"
            },
            "accessory": {
                "action_id": "channel_selected",
                "type": "channels_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a channel"
                },
            }
        }
    ]
    
    say(blocks=blocks)

def generate_section_selecting_gif_options(data):
    generated_options = []
    for i in range(len(data)):
        generated_options.append({
            "text": {
                "type": "plain_text",
                "text": str(i+1)
            },
            "value": data[i]["images"]["original"]["url"]
        })
    return generated_options

def generate_find_gif_blocks(command, data):
    generated_blocks = []
    for i in range(len(data)):
        generated_blocks.append({
            "type": "image",
            "title": {
                "type": "plain_text",
                "text": f"Choice {i+1}"
            },
            "block_id": f"image{i}",
            "alt_text": f"Choice {i+1} from Giphy search with {command['text']}",
            "image_url": data[i]["images"]["original"]["url"],
        })
    
    generated_options = generate_section_selecting_gif_options(data)

    generated_blocks.append({
        "type": "section",
        "block_id": "section_selecting_gif",
        "text": {
            "type": "mrkdwn",
            "text": "Pick your favourite gif from the dropdown list please!"
        },
        "accessory": {
            "action_id": "item_selected",
            "type": "static_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select a gif number"
            },
            "options": generated_options
        }
    })

    return generated_blocks


@app.command("/find-gif")
def find_gif(ack, say, command):
    ack()

    res = requests.get(f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_KEY}&limit=10&q={command['text']}")
    data = res.json()["data"]

    generated_blocks = generate_find_gif_blocks(command, data)

    say(blocks=generated_blocks)



def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


if __name__ == "__main__":
    main()