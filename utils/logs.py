import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PASTA_LOGS = BASE_DIR / "logs"

PASTA_LOGS.mkdir(exist_ok=True)

ARQUIVO_LOG = PASTA_LOGS / "autenticacao.log"

logger = logging.getLogger("rbac.autenticacao")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.FileHandler(
        ARQUIVO_LOG,
        encoding="utf-8"
    )

    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    handler.setFormatter(formato)
    logger.addHandler(handler)