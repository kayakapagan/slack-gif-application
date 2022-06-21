import logging
import os
import requests

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
GIPHY_KEY = os.environ["GIPHY_KEY"]



app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET, name="Joke Bot")
logger = logging.getLogger(__name__)





@app.command("/greet")
def message_greet(ack, say, command):
    ack()
    say(f"Hey {command['text']}")

# To learn available listener arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")

@app.message("hey")
def message_hey(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")

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
    

@app.command("/find-gif")
def find_gif(ack, say, command):
    ack()

    res = requests.get(f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_KEY}&limit=10&q={command['text']}")

    data = res.json()["data"]
    url = data[0]["images"]["original"]["url"]
    print(url)
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
            "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "1"
                        },
                        "value": data[0]["images"]["original"]["url"]
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "2"
                        },
                        "value": data[1]["images"]["original"]["url"]
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "3"
                        },
                        "value": data[2]["images"]["original"]["url"]
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "4"
                        },
                        "value": data[3]["images"]["original"]["url"]
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "5"
                        },
                        "value": data[4]["images"]["original"]["url"]
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "6"
                        },
                        "value": data[5]["images"]["original"]["url"]
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "7"
                        },
                        "value": data[6]["images"]["original"]["url"]
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "8"
                        },
                        "value": data[7]["images"]["original"]["url"]
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "9"
                        },
                        "value": data[8]["images"]["original"]["url"]
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "10"
                        },
                        "value": data[9]["images"]["original"]["url"]
                    }
            ]
        }
    })

    # blocks = [
    #     # {
	# 	# 	"type": "section",
	# 	# 	"block_id": "section567",
	# 	# 	"text": {
	# 	# 		"type": "mrkdwn",
	# 	# 		"text": "This is a section block with an accessory image."
	# 	# 	},
	# 	# 	"accessory": {
	# 	# 		"type": "image",
	# 	# 		"image_url": url,
	# 	# 		"alt_text": "cute cat"
	# 	# 	}
	# 	# },
    #     {
    #         "type": "image",
    #         "title": {
    #             "type": "plain_text",
    #             "text": "Please enjoy this photo of a kitten"
    #         },
    #         "block_id": "image4",
    #         "image_url": url,
    #         "alt_text": "An incredibly cute kitten."
    #     }
    # ]

    say(blocks=generated_blocks)



def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


if __name__ == "__main__":
    main()