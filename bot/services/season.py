import asyncio
from datetime import datetime, timezone
from bot.services.db import get_db

async def ensure_season_config():
    db = get_db()
    coll = db["season_config"]
    existing = await asyncio.to_thread(coll.find_one, {})
    if not existing:
        default_config = {
            "start_date": datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            "end_date": datetime(2026, 2, 5, 10, 24, 0, tzinfo=timezone.utc),
            "zero_norm_threshold": 15000
        }
        await asyncio.to_thread(coll.insert_one, default_config)
        print("✅ Создана начальная конфигурация сезона: 01.01.2026 – 05.02.2026 10:24 UTC")

async def get_season_config():
    db = get_db()
    coll = db["season_config"]
    return await asyncio.to_thread(coll.find_one, {})

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