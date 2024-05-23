import asyncio
import os
import time

from dotenv import load_dotenv

from pyslobs import ScenesService
from pyslobs.config import ConnectionConfig
from pyslobs.connection import SlobsConnection

load_dotenv()

SLOBS_HOST = os.environ.get("TWITCH_BOT_SLOBS_HOST", "192.168.1.98")
SLOBS_PORT = os.environ.get("TWITCH_BOT_SLOBS_PORT", 59650)
SLOBS_KEY = os.environ.get("TWITCH_BOT_SLOBS_KEY")
SLEEP_TIME = 15

if not SLOBS_KEY:
    raise exit("please set TWITCH_BOT_SLOBS_KEY to remote Streamlabs key")


async def change_scene(conn, scene_id, *args, **kwargs):
    ss = ScenesService(conn)

    current_scene = await ss.active_scene()
    if "animation" in current_scene.name.lower():
        print("Can't switch from logo animation scene")
        return
    await ss.make_scene_active(scene_id)
    time.sleep(SLEEP_TIME)
    await ss.make_scene_active(current_scene.id)
    conn.close()


async def run_slobs_function(func, *args, **kwargs):
    conn = SlobsConnection(
        ConnectionConfig(domain=SLOBS_HOST, token=SLOBS_KEY, port=SLOBS_PORT)
    )

    result = await asyncio.gather(conn.background_processing(), func(conn, *args))

    return result[1]


async def run_test_slobs_connection():
    async def _close(conn):
        conn.close()

    conn = SlobsConnection(
        ConnectionConfig(domain=SLOBS_HOST, token=SLOBS_KEY, port=SLOBS_PORT)
    )

    await asyncio.gather(conn.background_processing(), _close(conn))

    return
