from dataclasses import dataclass

@dataclass(frozen=True)
class SharePointConfig:
    SITE_URL: str = "https://company.sharepoint.com/sites/knowledgehub"
    DOCUMENT_LIBRARY: str = "Shared Documents"
    ROOT_FOLDER: str = "/AI-Training-Materials"
    ALLOWED_FILE_TYPES: tuple = ("pptx", "pdf", "mp4")


@dataclass(frozen=True)
class AppSettings:
    APP_NAME: str = "Enterprise Knowledge Assistant"
    MAX_CONTEXT_CHUNKS: int = 6
    MIN_RELEVANCE_SCORE: float = 0.75
    DEFAULT_LLM_PROVIDER: str = "openai"
    VOICE_ENABLED: bool = True
    ENABLE_INGESTION_ON_STARTUP: bool = False  # important for prod


SETTINGS = AppSettings()
SHAREPOINT = SharePointConfig()
