"""Shared config. Fill TODOs. Do not hardcode secrets."""

from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()

# TODO: read SAP_BASE_URL from environment with a default for local mock
SAP_BASE_URL = os.getenv("SAP_BASE_URL", "")

# TODO: resolve DATA_DIR relative to this project folder (idoc_selfheal_mock/)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
