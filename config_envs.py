import os
from dotenv import load_dotenv

load_dotenv(encoding="cp1252")


def _require(key:str)->str:
    value=os.getenv(key)
    if not value:
        raise EnvironmentError(
            f"Variável de ambiente obrigatória '{key}' não está definida. "
            f"Verifique o arquivo .env"
        )
    return value



class Config:
    dbname= _require("DB_NAME")
    user= _require("DB_USER")
    password= _require("DB_PASSWORD")
    host= _require("DB_HOST")
    port =_require("DB_PORT")

    SECRET_KEY = _require("SECRET_KEY")
    ALLOWED_HOSTS = _require("ALLOWED_HOSTS")
    SECURE_HSTS_SECONDS = _require("SECURE_HSTS_SECONDS")

    CORS_ALLOWED_ORIGINS=_require("CORS_ALLOWED_ORIGINS")

    DEBUG = os.getenv('DEBUG', 'False') == 'True'
