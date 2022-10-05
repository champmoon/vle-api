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
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def init() -> None:
    try:
        async with async_engine.connect() as conn:
            result = await conn.execute(sa.text("SELECT * FROM user;"))
            logger.info(result.fetchall())
        await async_engine.dispose()
    except Exception as e:
        logger.error(e)
        raise e


async def main() -> None:
    logger.info("Initializing service")
    await init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    asyncio.run(main())
