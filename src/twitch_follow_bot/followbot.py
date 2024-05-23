import asyncio
import os

from twitchAPI.eventsub.webhook import EventSubWebhook
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.helper import first
from twitchAPI.oauth import UserAuthenticationStorageHelper
from twitchAPI.object.eventsub import ChannelFollowEvent
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope

from twitch_follow_bot.services import (
    change_scene,
    run_slobs_function,
    run_test_slobs_connection,
)

CLIENT_ID = os.environ.get("TWITCH_BOT_TWITCH_CLIENT_ID")
CLIENT_SECRET = os.environ.get("TWITCH_BOT_TWITCH_CLIENT_SECRET")
TARGET_SCOPES = [AuthScope.MODERATOR_READ_FOLLOWERS]

if not CLIENT_ID or not CLIENT_SECRET:
    raise exit(
        "Please set TWITCH_BOT_TWITCH_CLIENT_ID and TWITCH_BOT_TWITCH_CLIENT_SECRET environment variables"
    )


async def on_follow(data: ChannelFollowEvent):
    # our event happend, lets do things with the data we got!
    print(f"{data.event.user_name} now follows {data.event.broadcaster_user_name}!")
    await run_slobs_function(change_scene, "scene_4a858596-50f6-4b65-adf4-f0522fc65460")


async def run():
    await run_test_slobs_connection()
    # create the api instance and get user auth either from storage or website
    twitch = await Twitch(CLIENT_ID, CLIENT_SECRET)
    helper = UserAuthenticationStorageHelper(twitch, TARGET_SCOPES)
    await helper.bind()

    # get the currently logged in user
    user = await first(twitch.get_users())

    # create eventsub websocket instance and start the client.
    eventsub = EventSubWebsocket(twitch)
    eventsub.start()
    # subscribing to the desired eventsub hook for our user
    # the given function (in this example on_follow) will be called every time this event is triggered
    # the broadcaster is a moderator in their own channel by default so specifying both as the same works in this example
    # We have to subscribe to the first topic within 10 seconds of eventsub.start() to not be disconnected.
    await eventsub.listen_channel_follow_v2(user.id, user.id, on_follow)
    # print(
    #     f"twitch event trigger channel.follow -F {EVENTSUB_URL}/callback -t {user.id} -u {follow_id} -s {eventsub.secret}"
    # )

    # eventsub will run in its own process
    # so lets just wait for user input before shutting it all down again
    try:
        input("press Enter to shut down...\n")
    except KeyboardInterrupt:
        pass
    finally:
        # stopping both eventsub as well as gracefully closing the connection to the API
        await eventsub.stop()
        await twitch.close()


asyncio.run(run())
