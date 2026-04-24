"""I/O helpers — safe parquet/CSV read-write with schema logging."""
from pathlib import Path

import pandas as pd


def save_table(df: pd.DataFrame, path: str | Path, index: bool = False) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".parquet":
        df.to_parquet(path, index=index)
    else:
        df.to_csv(path, index=index)


def load_table(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    elif path.suffix in (".xlsx", ".xls"):
        return pd.read_excel(path)
    else:
        return pd.read_csv(path)


def save_figure(fig, path: str | Path, dpi: int = 300) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
