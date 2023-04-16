from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from tides.routes import router
from tides.__version__ import __version__

from tides.dependencies import get_settings

import importlib.resources

settings = get_settings()


OPEN_API_URI = "/api/openapi.json"

ai_plugin_json = {
    "schema_version": "v1",
    "name_for_human": "Tide levels",
    "name_for_model": "tide_levels",
    # Hello fellow humans 👋
    "description_for_human": f"""Find out the current tides for any location in the world.
        """.strip(),
    # Hello fellow models 💃 🕺🏽
    "description_for_model": f"""
        Pull tide data from NOAA for any location in the world.
        """.strip(),
    "auth": settings.openai_plugin_auth(),
    "api": {
        "type": "openapi",
        "url": f"{settings.PLUGIN_DOMAIN}{OPEN_API_URI}",
        "is_user_authenticated": False,
    },
    "logo_url": settings.PLUGIN_LOGO,
    "contact_email": "rgbkrk@gmail.com",
    "legal_info_url": "https://github.com/rgbkrk",
}

app = FastAPI(
    title=ai_plugin_json["name_for_human"],
    description=ai_plugin_json["description_for_human"],
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
@app.get(OPEN_API_URI, include_in_schema=False)
async def get_openapi():
    return app.openapi()


@app.get("/.well-known/ai-plugin.json", include_in_schema=False)
async def get_ai_plugin_json():
    return ai_plugin_json


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
