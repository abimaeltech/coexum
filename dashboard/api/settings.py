from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl

class Settings(BaseSettings):
    api_port:         int         = 8000
    p2p_port:         int         = 9000
    registry_url:     AnyHttpUrl  = "https://registry.coexum.org"
    blockchain_rpc:   AnyHttpUrl  = "https://polygon-rpc.com"
    schedule_interval:int         = 30

    class Config:
        env_file = ".env"      # aponta pro seu .env
        env_prefix = ""        # sem prefixo, pega exatamente as chaves acima

settings = Settings()
