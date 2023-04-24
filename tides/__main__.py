import asyncio

import uvicorn

from tides.app import app
from tides.dependencies import get_settings

settings = get_settings()


async def main():
    if settings.local_dev():
        host = "127.0.0.1"
    else:
        host = "0.0.0.0"

    config = uvicorn.Config(
        app=app,
        host=host,
        port=int(settings.PLUGIN_PORT),
        log_level="info",
    )
    server = uvicorn.Server(config)

    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
