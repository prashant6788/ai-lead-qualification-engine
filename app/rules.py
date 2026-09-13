from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


DEFAULT_RULES_PATH = Path(__file__).resolve().parents[1] / "config" / "qualification-rules.json"


@lru_cache(maxsize=1)
def load_rules(path: str | None = None) -> dict[str, Any]:
    rules_path = Path(path) if path else DEFAULT_RULES_PATH
    with rules_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    required_sections = {"supported_services", "scoring", "thresholds"}
    missing = required_sections - set(data)
    if missing:
        raise ValueError(f"Missing required rule sections: {sorted(missing)}")

    return data


def normalize_service(value: str | None) -> str | None:
    if not value:
        return None
    return (
        value.strip()
        .lower()
        .replace("&", "and")
        .replace("/", "_")
        .replace("-", "_")
        .replace(" ", "_")
    )


def is_supported_service(service: str | None, rules: dict[str, Any]) -> bool:
    normalized = normalize_service(service)
    supported = {normalize_service(item) for item in rules["supported_services"]}
    return normalized in supported
