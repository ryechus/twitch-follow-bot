# Twitch Follow Bot

This is a bot that runs locally and will change Streamlabs scenes whenever a user follows a twitch channel.

## Usage

### Installation

    pip install .

### Running

Create a `.env` env file with the following contents

```
TWITCH_BOT_SLOBS_KEY=api_token_from_streamlabs_desktop_remote_control_settings
TWITCH_BOT_TWITCH_CLIENT_ID=twitch_app_client_id
TWITCH_BOT_TWITCH_CLIENT_SECRET=twitch_app_client_secret
```

Run the bot

```bash
python -m twitch_follow_bot.followbot
```

You should see this

```bash
press Enter to shut down...
```

Whenever a user follows you should see this

```bash
user now follows channel!
```