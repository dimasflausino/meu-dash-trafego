"""
Configurações centralizadas do Analytics Pro SaaS.
Segue as melhores práticas de 12-factor app.
"""

from typing import Optional
from dataclasses import dataclass
from enum import Enum
import os
from pathlib import Path


class Environment(str, Enum):
    """Ambientes suportados"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass
class StreamlitConfig:
    """Configurações do Streamlit"""
    page_title: str = "Analytics Pro SaaS"
    layout: str = "wide"
    initial_sidebar_state: str = "expanded"
    theme_primary_color: str = "#00ffcc"
    theme_background_color: str = "#0b0e14"
    theme_secondary_background_color: str = "#111827"
    theme_text_color: str = "#ffffff"


@dataclass
class DatabaseConfig:
    """Configurações de banco de dados"""
    provider: str = "gsheets"  # gsheets, postgresql, sqlite
    gsheets_url: Optional[str] = None
    gsheets_worksheet: str = "Configuracoes"
    cache_ttl: int = 300  # 5 minutos


@dataclass
class APIConfig:
    """Configurações de APIs externas"""
    meta_api_version: str = "v24.0"
    google_api_version: str = "v13"
    tiktok_api_version: str = "v1"
    request_timeout: int = 30
    max_retries: int = 3


@dataclass
class LogConfig:
    """Configurações de logging"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None


class Settings:
    """Classe principal de configurações"""

    def __init__(self):
        self.env = Environment(os.getenv("ENV", Environment.DEVELOPMENT.value))
        self.debug = self.env == Environment.DEVELOPMENT
        
        # Configurações específicas
        self.streamlit = StreamlitConfig()
        self.database = DatabaseConfig(
            gsheets_url=os.getenv("GSHEETS_URL"),
        )
        self.api = APIConfig()
        self.log = LogConfig(
            level=os.getenv("LOG_LEVEL", "INFO"),
            file=os.getenv("LOG_FILE"),
        )
        
        # Caminhos
        self.base_dir = Path(__file__).parent.parent
        self.src_dir = self.base_dir / "src"
        self.data_dir = self.base_dir / "data"
        self.config_dir = self.base_dir / "config"
        
        # Secrets (nunca commitar!)
        self.meta_token = os.getenv("META_TOKEN")
        self.google_dev_token = os.getenv("GOOGLE_DEV_TOKEN")
        self.tiktok_token = os.getenv("TIKTOK_TOKEN")
        self.hotmart_secret = os.getenv("HOTMART_SECRET")
        self.kiwify_token = os.getenv("KIWIFY_TOKEN")


# Instância global
settings = Settings()
