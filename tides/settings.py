import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    PLUGIN_ENV: str = "dev"
    PLUGIN_PORT: str = "8182"

    @property
    def PLUGIN_SERVER_DESCRIPTION(self) -> str:
        from_env = os.environ.get("PLUGIN_SERVER_DESCRIPTION")
        if from_env:
            return from_env

        if self.is_dev():
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
        return f"http://localhost:{self.PLUGIN_PORT}"

    def openai_plugin_auth(self):
        return {"type": "no_auth"}
        # if self.is_dev():
        #     # When using localhost, we are forced to use no auth
        #     return {"type": "no_auth"}
        # else:
        #     return {
        #         "type": "user_http",
        #         "authorization_type": "bearer",
        #     }

    def is_dev(self):
        return self.PLUGIN_ENV == "dev"
