# bot/services/season.py
import asyncio
from datetime import datetime, timezone
from bot.services.db import init_season_config, get_season_config

async def ensure_season_config():
    # Инициализация сезона при старте
    from config import DB_PATH
    init_season_config(
        start="2026-01-01 00:00:00",
        end="2026-02-05 10:24:00",
        threshold=15000
    )

async def get_season_config_async():
    return get_season_config()

def calculate_progress(season, user, current_trophies: int):
    from config import NORM
    custom_norm = user.get("custom_norm")
    norm = custom_norm if custom_norm is not None else NORM

    if current_trophies >= season["zero_norm_threshold"]:
        norm = 0

    start_trophies = user["season_start_trophies"]
    gained = current_trophies - start_trophies
    done = gained >= norm
    percent = round(gained / norm * 100, 1) if norm > 0 else 100.0
    percent = min(100.0, percent)

    return {
        "norm": norm,
        "start": start_trophies,
        "current": current_trophies,
        "gained": gained,
        "done": done,
        "percent": percent
    }
