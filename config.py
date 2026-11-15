import os
from pathlib import Path

from dotenv import load_dotenv

# # Root
ROOT_DIR = Path(__file__).parent
MEDIA_FILES_DIR = ROOT_DIR / "files" / "media_files"


# Load variables from .env
load_dotenv()


# Environment URL settings
def get_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} is not set")
    return value


class Config:
    # ENV
    ENV = os.getenv("ENV", "dev")
    SHOW_LOGS = os.getenv("SHOW_LOGS", "false").lower() == "true"

    # tasks UI url
    FRONT_URLS_UI = {
        "dev": get_env("FRONT_DEV_URL_UI"),
        "stage": get_env("FRONT_STAGE_URL_UI"),
    }

    BASE_FRONT_URL_UI = FRONT_URLS_UI[ENV]

    # Credentials
    ADMIN_LOGIN = get_env("ADMIN_LOGIN")
    ADMIN_PASSWORD = get_env("ADMIN_PASSWORD")
