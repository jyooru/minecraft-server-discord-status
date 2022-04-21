import asyncio
from argparse import ArgumentParser, Namespace
from os import environ
from typing import Any, List, Optional

import aiohttp
from discord import AsyncWebhookAdapter, Webhook
from mcstatus import JavaServer

from . import MinecraftServerDiscordStatus


def environ_or_required(key: str) -> Any:
    # https://stackoverflow.com/a/45392259
    return {"default": environ.get(key)} if environ.get(key) else {"required": True}


def parse_args(args: Optional[List[str]] = None) -> Namespace:
    parser = ArgumentParser(
        description="Updates a Discord message with the status of a Minecraft server"
    )
    parser.add_argument(
        "--message-id",
        help="ID of the Discord message to edit",
        type=int,
        **environ_or_required("MESSAGE_ID"),
    )
    parser.add_argument(
        "--server-host",
        help="Host of the Minecraft server to check",
        **environ_or_required("SERVER_HOST"),
    )
    parser.add_argument(
        "--server-port",
        default=environ.get("SERVER_PORT"),
        help="Port of the Minecraft server to check",
        type=int,
    )
    parser.add_argument(
        "--sleep",
        default=environ.get("SLEEP"),
        help="Delay between updates",
        type=int,
    )
    parser.add_argument(
        "--thumbnail",
        default=environ.get("THUMBNAIL"),
        help="URL of the thumbnail to use in the Discord embed",
    )
    parser.add_argument(
        "--title",
        default=environ.get("TITLE"),
        help="Title of the Discord embed",
    )
    parser.add_argument(
        "--webhook",
        help="URL of the Discord webhook",
        **environ_or_required("WEBHOOK"),
    )

    if args is None:
        return parser.parse_args()
    return parser.parse_args(args)


async def async_main() -> None:
    args = parse_args()
    async with aiohttp.ClientSession() as session:
        status = MinecraftServerDiscordStatus(
            message_id=args.message_id,
            server=JavaServer(args.server_host, args.server_port or 25565),
            webhook=Webhook.from_url(
                args.webhook,
                adapter=AsyncWebhookAdapter(session),
            ),
            title=args.title,
            thumbnail=args.thumbnail,
        )

        while True:
            await status.update()
            await asyncio.sleep(args.sleep or 30)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
