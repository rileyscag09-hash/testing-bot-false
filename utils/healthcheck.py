import os
from contextlib import suppress

from aiohttp import web

from utils.constants import logger


async def _handle_root(_: web.Request) -> web.Response:
    return web.json_response({"status": "ok", "service": "epn-discord-bot"})


async def start_healthcheck_server() -> web.AppRunner | None:
    """Start a tiny HTTP server for hosts that require an open port."""
    port = int(os.getenv("PORT", "8080"))
    host = os.getenv("HOST", "0.0.0.0")

    app = web.Application()
    app.router.add_get("/", _handle_root)
    app.router.add_get("/health", _handle_root)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, host=host, port=port)
    await site.start()
    logger.info(f"Healthcheck server listening on {host}:{port}")
    return runner


async def stop_healthcheck_server(runner: web.AppRunner | None) -> None:
    if runner is None:
        return

    with suppress(Exception):
        await runner.cleanup()
