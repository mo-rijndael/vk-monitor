from asyncio import sleep
import logging
import html

from pydantic import parse_obj_as
from aiohttp import ClientSession
import websockets

from models import Credentials, Rule, WsEvent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")


async def authorise(http: ClientSession, token: str) -> Credentials:
    async with http.post("https://api.vk.com/method/streaming.getServerUrl", data={
        "v": 5.131,
        "access_token": token
    }) as response:
        response = await response.json()
        parsed = Credentials.parse_obj(response["response"])
        logger.info("Authorisation successful")
        return parsed


async def get_rules(http: ClientSession, creds: Credentials) -> list[Rule]:
    async with http.get(f"https://{creds.endpoint}/rules?key={creds.key}") as response:
        response = await response.json()
        print(response)
        if response["rules"]:
            return parse_obj_as(list[Rule], response["rules"])
        return []


async def delete_rule(http: ClientSession, creds: Credentials, tag: str):
    await http.delete(f"https://{creds.endpoint}/rules?key={creds.key}", json={"tag": tag})


async def add_rule(http: ClientSession, creds: Credentials, rule: Rule):
    await http.post(f"https://{creds.endpoint}/rules?key={creds.key}", json={"rule": rule.dict()})


async def listen(creds: Credentials):
    url = f"wss://{creds.endpoint}/stream?key={creds.key}"
    ws = await websockets.connect(url)
    # такая страшная конструкция для авто-реконнекта
    logger.info("Connected to stream")
    while True:
        try:
            data = await ws.recv()
        except websockets.ConnectionClosedError:
            logger.warn("Websocket closed, reconnecting")
            await sleep(10)
            ws = await websockets.connect(url)
            continue
        event = WsEvent.parse_raw(data).event
        if not event:
            continue
        event.text = html.unescape(event.text).replace("<br>", "\n")
        yield event
