from typing import Optional
from mcstatus import JavaServer
from mcstatus.pinger import PingResponse
from discord import Webhook, Embed, Color
from datetime import datetime, timezone
from asyncio import TimeoutError


class MinecraftServerDiscordStatus:
    def __init__(
        self,
        message_id: int,
        server: JavaServer,
        webhook: Webhook,
        thumbnail: Optional[str] = None,
        title: str = "Minecraft Server Status",
    ) -> None:
        self.message_id = message_id  # discord message to edit
        self.server = server  # minecraft server to check
        self.webhook = webhook  # discord webhook to use
        self.thumbnail = thumbnail  # thumbnail for discord embed
        self.title = title  # title for discord embed

    def generate_embed(
        self,
        response: Optional[PingResponse] = None,
        updated: Optional[datetime] = None,
    ) -> Embed:
        if updated is None:
            updated = datetime.now()

        online = response is not None

        embed = Embed(
            title=self.title,
            description="Currently " + ("online!" if online else "offline."),
            color=Color.green() if online else Color.red(),
        )
        if self.thumbnail is not None:
            embed.set_thumbnail(url=self.thumbnail)
        embed.add_field(
            name="Host",
            value=f"{self.server.address.host}",
        )
        if online:
            embed.add_field(name="Latency", value=str(int(response.latency)) + "ms")
            players_field = f"{response.players.online}/{response.players.max}"
            if response.players.sample is not None:
                players_field += "\n```"
                for player in response.players.sample:
                    players_field += f"\n{player.name}"
                players_field += "\n```"
            embed.add_field(
                name="Players",
                value=players_field,
                inline=False,
            )
        embed.set_footer(
            text="Last updated at "
            + updated.replace(microsecond=0, tzinfo=timezone.utc)
            .isoformat(sep=" ")  # everyone can understand this
            .replace("+00:00", " (UTC)")  # make it a little easier
        )
        return embed

    async def update(self):
        response = None
        try:
            response = await self.server.async_status()
        except OSError:
            pass
        except TimeoutError:
            pass

        embed = self.generate_embed(response)
        await self.webhook.edit_message(self.message_id, content="", embed=embed)
