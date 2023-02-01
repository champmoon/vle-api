from pydantic import BaseSettings


class ToolsSettings(BaseSettings):
    FOLDERS_FOR_LINTING: list[str] = ["app"]
    FOLDERS_FOR_FORMATTING: list[str] = ["app"]


settings = ToolsSettings()
