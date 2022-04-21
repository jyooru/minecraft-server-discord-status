from . import MinecraftServerDiscordStatus
import asyncio
from mcstatus import JavaServer
from discord import Webhook, AsyncWebhookAdapter
import aiohttp


async def async_main() -> None:
    async with aiohttp.ClientSession() as session:
        statuses = [
            MinecraftServerDiscordStatus(
                message_id=966597522518867988,
                server=JavaServer("raiblocksmc-play.com"),
                webhook=Webhook.from_url(
                    "https://discord.com/api/webhooks/966597376053739580/no",
                    adapter=AsyncWebhookAdapter(session),
                ),
                title="RaiblocksMC Status",
                thumbnail="https://raiblocksmc.com/storage/img/bigbigicon.png",
            ),
            MinecraftServerDiscordStatus(
                message_id=966608694521528320,
                server=JavaServer("example.com"),
                webhook=Webhook.from_url(
                    "https://discord.com/api/webhooks/966608280594026566/no",
                    adapter=AsyncWebhookAdapter(session),
                ),
            ),
        ]

        while True:
            await asyncio.gather(*[status.update() for status in statuses])
            await asyncio.sleep(30)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
