import os
import json
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
    say(
        channel=body["actions"][0]["selected_channel"],
        blocks=[
            {
                "type": "image",
                "title": {"type": "plain_text", "text": "Enjoy your gif"},
                "block_id": "image_selected",
                "alt_text": "selected image from Giphy.",
                "image_url": body["actions"][0]["block_id"],
            }
        ],
    )


@app.action("channel_selected_in_modal")
def action_channel_selected_in_modal(_, ack):
    # Acknowledge the action
    ack()


@app.action("normal_item_selected")
def action_normal_item_selected(body, ack, say):
    # Acknowledge the action
    ack()
    blocks = [
        {
            "type": "section",
            "block_id": body["actions"][0]["selected_option"]["value"],
            "text": {"type": "mrkdwn", "text": "Pick a channel from the dropdown list"},
            "accessory": {
                "action_id": "channel_selected",
                "type": "channels_select",
                "placeholder": {"type": "plain_text", "text": "Select a channel"},
            },
        }
    ]

    say(blocks=blocks)


def generate_section_selecting_gif_options(data):
    generated_options = []
    for i in range(len(data)):
        generated_options.append(
            {
                "text": {"type": "plain_text", "text": str(i + 1)},
                "value": data[i]["images"]["original"]["url"],
            }
        )
    return generated_options


def generate_find_gif_blocks(search_query, data, static_select_action_id):
    generated_blocks = []
    for i in range(len(data)):
        generated_blocks.append(
            {
                "type": "image",
                "title": {"type": "plain_text", "text": f"Choice {i+1}"},
                "block_id": f"image{i}",
                "alt_text": f"Choice {i+1} from Giphy search with {search_query}",
                "image_url": data[i]["images"]["original"]["url"],
            }
        )

    generated_options = generate_section_selecting_gif_options(data)

    generated_blocks.append(
        {
            "type": "section",
            "block_id": "section_selecting_gif",
            "text": {
                "type": "mrkdwn",
                "text": "Pick your favourite gif from the dropdown list please!",
            },
            "accessory": {
                "action_id": static_select_action_id,
                "type": "static_select",
                "placeholder": {"type": "plain_text", "text": "Select a gif number"},
                "options": generated_options,
            },
        }
    )

    return generated_blocks


@app.command("/find-gif")
def find_gif(ack, say, command):
    ack()
    res = requests.get(
        f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_KEY}&limit=10&q={command['text']}"
    )
    data = res.json()["data"]

    generated_blocks = generate_find_gif_blocks(
        command["text"], data, "normal_item_selected"
    )

    say(blocks=generated_blocks)


@app.action("modal_item_selected")
def action_modal_item_selected_update(ack, body, client):
    # Acknowledge the button request
    ack()

    blocks = [
        {
            "type": "section",
            "block_id": body["actions"][0]["selected_option"]["value"],
            "text": {"type": "mrkdwn", "text": "Pick a channel from the dropdown list"},
            "accessory": {
                "action_id": "channel_selected",
                "type": "channels_select",
                "placeholder": {"type": "plain_text", "text": "Select a channel"},
            },
        }
    ]

    # Call views_update with the built-in client
    client.views_update(
        # Pass the view_id
        view_id=body["view"]["id"],
        # String that represents view state to protect against race conditions
        hash=body["view"]["hash"],
        # View payload with updated blocks
        view={
            "type": "modal",
            # View identifier
            "callback_id": "view_1",
            "title": {"type": "plain_text", "text": "Updated modal"},
            "blocks": blocks,
        },
    )


@app.action("gif_selected_in_modal")
def action_gif_selected_in_modal(ack, body, say):
    # Acknowledge the button request
    ack()

    value = json.loads(body["actions"][0]["value"])
    channel_id = value["channel_id"]
    url = value["url"]

    say(
        channel=channel_id,
        blocks=[
            {
                "type": "image",
                "title": {"type": "plain_text", "text": "Enjoy your gif"},
                "block_id": "image_selected",
                "alt_text": "selected image from Giphy.",
                "image_url": url,
            }
        ],
    )


@app.view("modal-for-search-input")
def search_submit(ack, body):
    search_query = body["view"]["state"]["values"]["search_input_modal_block_id"][
        "sl_input"
    ]["value"]

    selected_channel_id = body["view"]["state"]["values"]["channel_selection_block_id"][
        "channel_selected_in_modal"
    ]["selected_channel"]

    res = requests.get(
        f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_KEY}&limit=10&q={search_query}"
    )
    data = res.json()["data"]

    # generated_blocks = generate_find_gif_blocks(
    #     search_query, data, "modal_item_selected"
    # )

    generated_blocks = []
    for i in range(len(data)):
        generated_blocks.append(
            {
                "type": "image",
                "title": {"type": "plain_text", "text": f"Choice {i+1}"},
                "block_id": f"image{i}",
                "alt_text": f"Choice {i+1} from Giphy search with {search_query}",
                "image_url": data[i]["images"]["original"]["url"],
            }
        )
        generated_blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"Press send to the choice {i+1}",
                },
                "accessory": {
                    "action_id": "gif_selected_in_modal",
                    "type": "button",
                    "text": {"type": "plain_text", "text": "send"},
                    "value": json.dumps(
                        {
                            "url": data[i]["images"]["original"]["url"],
                            "channel_id": selected_channel_id,
                        }
                    ),
                },
            }
        )

    ack(
        response_action="push",
        view={
            "type": "modal",
            # View identifier
            # "callback_id": "view_1",
            "title": {"type": "plain_text", "text": "Updated modal"},
            "blocks": generated_blocks,
        },
    )


# The open_modal shortcut listens to a shortcut with the callback_id "open_modal"
@app.shortcut("search_shortcut")
def search_shortcut(ack, shortcut, client):
    # Acknowledge the shortcut request
    ack()
    # Call the views_open method using the built-in WebClient
    client.views_open(
        trigger_id=shortcut["trigger_id"],
        # A simple view payload for a modal
        view={
            "type": "modal",
            "callback_id": "modal-for-search-input",
            "title": {"type": "plain_text", "text": "Search a Gif!"},
            "close": {"type": "plain_text", "text": "Close"},
            "submit": {"type": "plain_text", "text": "Search"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "search_input_modal_block_id",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "sl_input",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "happy cat",
                        },
                    },
                    "label": {"type": "plain_text", "text": "Search"},
                    "hint": {
                        "type": "plain_text",
                        "text": "Write your search query please.",
                    },
                },
                {
                    "type": "section",
                    "block_id": "channel_selection_block_id",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Pick a channel from the dropdown list",
                    },
                    "accessory": {
                        "action_id": "channel_selected_in_modal",
                        "type": "channels_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a channel",
                        },
                    },
                },
            ],
        },
    )


def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


if __name__ == "__main__":
    main()
