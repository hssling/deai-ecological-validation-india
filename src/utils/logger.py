"""Structured logger writing to logs/progress.md and stdout."""
import logging
import sys
from datetime import datetime
from pathlib import Path


def get_logger(name: str, log_dir: str | Path = "logs") -> logging.Logger:
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                                datefmt="%Y-%m-%d %H:%M:%S")
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(fmt)
        logger.addHandler(sh)

        fh = logging.FileHandler(log_dir / "pipeline.log")
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger


def log_phase(phase_name: str, status: str, notes: str = "",
              log_dir: str | Path = "logs") -> None:
    """Append a structured entry to logs/progress.md."""
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    md_path = log_dir / "progress.md"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"\n## {phase_name} — {status}\n"
        f"**Timestamp:** {timestamp}\n\n"
        f"{notes}\n\n"
        f"---\n"
    )
    with open(md_path, "a") as f:
        f.write(entry)
