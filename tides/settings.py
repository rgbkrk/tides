import os
from typing import Optional
from functools import cached_property
from pydantic import BaseSettings


class Settings(BaseSettings):
    PLUGIN_ENV: str = "dev"
    PLUGIN_PORT: str = "8182"

    OPEN_API_URI: str = "/api/openapi.json"

    @property
    def PLUGIN_SERVER_DESCRIPTION(self) -> str:
        from_env = os.environ.get("PLUGIN_SERVER_DESCRIPTION")
        if from_env:
            return from_env

        if self.local_dev():
            return f"Local Tide Server (dev)"

        return f"Tide Server"

    @property
    def PLUGIN_LOGO(self) -> str:
        from_env = os.environ.get("PLUGIN_LOGO")
        if from_env:
            return from_env

        return f"{self.PLUGIN_DOMAIN}/static/images/surf.svg"

    @property
    def PLUGIN_DOMAIN(self) -> str:  # noqa
        from_env = os.environ.get("PLUGIN_DOMAIN")
        if from_env:
            return from_env

        if self.is_vercel():
            return f"https://{os.environ.get('VERCEL_URL')}"

        return f"http://localhost:{self.PLUGIN_PORT}"

    def is_vercel(self) -> bool:
        return os.environ.get("VERCEL") == "1"

    def openai_plugin_auth(self):
        return {"type": "no_auth"}

    def local_dev(self):
        return self.PLUGIN_ENV == "dev"

    @cached_property
    def ai_plugin_json(self):
        return {
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
            "auth": self.openai_plugin_auth(),
            "api": {
                "type": "openapi",
                "url": f"{self.PLUGIN_DOMAIN}{self.OPEN_API_URI}",
                "is_user_authenticated": False,
            },
            "logo_url": self.PLUGIN_LOGO,
            "contact_email": "rgbkrk@gmail.com",
        }

    class Config:
        env_file = ".env"

        keep_untouched = (cached_property,)
