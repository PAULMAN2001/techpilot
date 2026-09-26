from pathlib import Path
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parents[2]
engine = create_engine(f"sqlite:///{BASE_DIR / 'techpilot.db'}", connect_args={"check_same_thread": False})


def init_db() -> None:
    # The database is intentionally minimal in Phase 1; history models come later.
    with engine.begin():
        pass