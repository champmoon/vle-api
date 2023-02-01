import asyncio
import logging

import sqlalchemy as sa
from tenacity import retry
from tenacity.after import after_log
from tenacity.before import before_log
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_fixed

from app.db.session import async_engine

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("pre_start/check-health")

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def health() -> None:
    try:
        async with async_engine.connect() as conn:
            await conn.execute(sa.text("SELECT * FROM user;"))
            logger.info("ok...")
        await async_engine.dispose()

    except Exception as e:
        logger.info("error...")
        logger.error(e)
        raise e


if __name__ == "__main__":
    asyncio.run(health())
