from typing import Optional

from create_bot import logger, r


class RedisConnector:
    rds = r

    @classmethod
    def redis_start(cls):
        # cls.rds.set('catalog', '')
        logger.info('Redis connected OKK')

    @classmethod
    async def update_catalog(cls, file_id: str):
        cls.rds.set('catalog', file_id)

    @classmethod
    async def get_catalog(cls) -> Optional[str]:
        response = cls.rds.get('catalog')
        if response is None or response == '':
            return None
        response = cls.rds.get('catalog').decode('utf=8')
        return response
