# bot/services/season.py
import asyncio
from datetime import datetime, timezone
from bot.services.db import init_season_config as _init_season_config
from bot.services.db import get_season_config as _get_season_config
from bot.services.db import update_season_config as _update_season_config
from config import NORM

async def ensure_season_config():
    """
    Инициализирует конфигурацию сезона при первом запуске.
    Сезон по умолчанию: 01.01.2026 00:00:00 — 05.02.2026 10:24:00 UTC
    """
    from bot.services.db import init_season_config
    init_season_config(
        start="2026-01-01 00:00:00",
        end="2026-02-05 10:24:00",
        threshold=15000
    )

async def get_season_config_async():
    """
    Асинхронная обёртка для получения конфигурации сезона.
    """
    return _get_season_config()

def calculate_progress(season, user, current_trophies: int):
    """
    Рассчитывает сезонный прогресс игрока.
    
    :param season: dict с ключами start_date, end_date, zero_norm_threshold
    :param user: dict с ключами season_start_trophies, custom_norm
    :param current_trophies: текущее количество трофеев
    :return: dict с прогрессом
    """
    custom_norm = user.get("custom_norm")
    norm = custom_norm if custom_norm is not None else NORM

    # Если кубков >= порога — норма = 0
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

