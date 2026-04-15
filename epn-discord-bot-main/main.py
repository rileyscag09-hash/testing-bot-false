"""
Entry point for the application.
"""
import asyncio
import sys

from EPN import run
from utils.constants import logger
from utils.healthcheck import start_healthcheck_server, stop_healthcheck_server


if __name__ == "__main__":
    try:
        async def main():
            healthcheck_runner = await start_healthcheck_server()
            try:
                await run()
            finally:
                await stop_healthcheck_server(healthcheck_runner)

        asyncio.run(main())
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        sys.exit()
    except Exception as e:
        logger.critical(e)
