import json
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent

def get_secret(
    key: str,
    default_value: Optional[str] = None,
    json_path: str = str(BASE_DIR / "secrets.json")
):
    with open(json_path) as f:
        secrets = json.loads(f.read())
    try:
        return secrets[key]
    except KeyError:
        if default_value:
            return default_value
        raise EnvironmentError(f"Set the {key} environment variable.")

MYSQL_USER = get_secret("MYSQL_USER")
MYSQL_PASSWORD = get_secret("MYSQL_PASSWORD")
MYSQL_HOST = get_secret("MYSQL_HOST")
MYSQL_PORT = get_secret("MYSQL_PORT")
MYSQL_DB = get_secret("MYSQL_DB")
MYSQL_DB_URL = f"mysql+asyncmy://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

NAVER_API_ID = get_secret("NAVER_API_ID")
NAVER_API_SECRET = get_secret("NAVER_API_SECRET")

