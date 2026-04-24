"""Central config loader — all scripts import this."""
import argparse
from pathlib import Path
import yaml


def load_config(config_path: str | Path = "config.yaml") -> dict:
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    # Resolve all path values to absolute Path objects relative to config location
    root = config_path.parent
    for key, val in cfg.get("paths", {}).items():
        cfg["paths"][key] = root / val
        cfg["paths"][key].mkdir(parents=True, exist_ok=True)
    return cfg


def get_arg_config() -> dict:
    """Parse --config CLI arg and return loaded config dict."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--config", default="config.yaml")
    args, _ = parser.parse_known_args()
    return load_config(args.config)
