from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from tides.routes import router
from tides.__version__ import __version__

from tides.dependencies import get_settings

import importlib.resources

settings = get_settings()


app = FastAPI(
    title=settings.ai_plugin_json["name_for_human"],
    description=settings.ai_plugin_json["description_for_human"],
    version=__version__,
    servers=[
        {
            "url": settings.PLUGIN_DOMAIN,
            "description": settings.PLUGIN_SERVER_DESCRIPTION,
        }
    ],
)

app.include_router(router)

static_directory = importlib.resources.files("tides") / "static"
app.mount("/static", StaticFiles(directory=str(static_directory)), name="static")


@app.get("/", include_in_schema=False)
async def get_root() -> HTMLResponse:
    return HTMLResponse(
        """
<img src="/static/images/surf.svg" alt="Surfboard at the beach" width="200" />
<h1>Enable Tides in ChatGPT!</h1>
"""
    )


# Defined outside of the router so we can call app.openapi()
@app.get(settings.OPEN_API_URI, include_in_schema=False)
async def get_openapi():
    return app.openapi()


@app.get("/.well-known/ai-plugin.json", include_in_schema=False)
async def get_ai_plugin_json():
    return settings.ai_plugin_json


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
