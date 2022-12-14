from argparse import ArgumentParser
import asyncio
import re

from aiohttp import ClientSession

from models import Config, Rule, Credentials, Event
import api


def is_trash(event: Event) -> bool:
    return event.event_type not in ["post", "comment"]


async def main():
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", type=open, required=True)
    parser.add_argument("-o", "--overwrite", default=False, action="store_true")
    args = parser.parse_args()
    config = Config.parse_raw(args.config.read())
    mention = re.compile(r"\[(?:id|club|public)\d+\|(.*)]")

    async with ClientSession() as http:
        http: ClientSession
        credentials = await api.authorise(http, config.vk_token)
        if args.overwrite:
            return await overwrite(http, credentials, config.rules)
        async for event in api.listen(credentials):
            if is_trash(event):
                continue
            event.text = mention.sub(r'\g<1>', event.text)
            for chat in config.notified:
                await http.post(f"https://api.telegram.org/bot{config.tg_token}/sendMessage", data={
                    "chat_id": chat,
                    "text": f"{event.event_url}\n\n"
                            f"{event.text}\n\n"
                            f"{str.join(' ', event.tags)}",
                    "disable_web_page_preview": True
                })


async def overwrite(http: ClientSession, creds: Credentials, rules: dict[str, str]):
    deletions = []
    insertions = []
    for rule in await api.get_rules(http, creds):
        deletions.append(api.delete_rule(http, creds, rule.tag))
    await asyncio.gather(*deletions)

    for tag, value in rules.items():
        rule = Rule(tag=tag, value=value)
        insertions.append(api.add_rule(http, creds, rule))
    await asyncio.gather(*insertions)


if __name__ == "__main__":
    asyncio.run(main())
