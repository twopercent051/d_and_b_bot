from datetime import datetime
from typing import Optional

from sqlalchemy import MetaData, inspect, Column, String, insert, select, update, Integer, func, TIMESTAMP
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, as_declarative

from create_bot import DATABASE_URL

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@as_declarative()
class Base:
    metadata = MetaData()

    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class DBRequests(Base):
    """Заявки на просмотр общего каталога"""
    __tablename__ = 'db_requests'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    type_request = Column(String, nullable=False)
    add_datetime = Column(TIMESTAMP, nullable=False, server_default=func.now())
    property_type = Column(String, nullable=True)  # Тип недвижимости
    target = Column(String, nullable=True)  # Цель инвестиций
    stage_building = Column(String, nullable=True)  # Этап строительства
    price = Column(String, nullable=True)  # Ценовой диапазон
    time_to_call = Column(String, nullable=True)  # Время для звонка


class DBRequestsDAO(DBRequests):
    """Класс взаимодействия с БД"""
    @classmethod
    async def create(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(DBRequests).values(**data)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def get_all(cls, limit: Optional[int] = None) -> list:
        async with async_session_maker() as session:
            if limit:
                query = select(DBRequests.__table__.columns).order_by(DBRequests.add_datetime.desc()).limit(limit)
            else:
                query = select(DBRequests.__table__.columns).order_by(DBRequests.add_datetime.desc())
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def get_one_or_none(cls, request_id: int) -> dict:
        async with async_session_maker() as session:
            query = select(DBRequests.__table__.columns).filter_by(id=request_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()
