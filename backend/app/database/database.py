from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

BASE_DIR = Path(__file__).resolve().parents[2]
engine = create_engine(f"sqlite:///{BASE_DIR / 'techpilot.db'}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class DiagnosticRun(Base):
    __tablename__ = "diagnostic_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    hostname = Column(String, nullable=False)
    status = Column(String, nullable=False, default="ok")
    finding_count = Column(Integer, nullable=False, default=0)
    findings = relationship("FindingRecord", back_populates="diagnostic_run", cascade="all, delete-orphan")


class FindingRecord(Base):
    __tablename__ = "findings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    diagnostic_run_id = Column(String, ForeignKey("diagnostic_runs.id"), nullable=False)
    category = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True, default="")
    evidence = Column(String, nullable=True, default="")
    recommendation = Column(String, nullable=True, default="")
    source = Column(String, nullable=True, default="")
    diagnostic_run = relationship("DiagnosticRun", back_populates="findings")


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def serialize_run(run: DiagnosticRun) -> dict:
    return {
        "id": run.id,
        "timestamp": run.timestamp.isoformat() if run.timestamp else None,
        "hostname": run.hostname,
        "status": run.status,
        "finding_count": run.finding_count,
        "findings": [
            {
                "id": finding.id,
                "category": finding.category,
                "severity": finding.severity,
                "title": finding.title,
                "description": finding.description,
                "evidence": finding.evidence,
                "recommendation": finding.recommendation,
                "source": finding.source,
            }
            for finding in (run.findings or [])
        ],
    }
