from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Float

DATABASE_URL = "sqlite+aiosqlite:///database.db"

Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    lastname = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    number = Column(String)
    password = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    tariff = Column(String, default="-")

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, lastname={self.lastname}, firstname={self.firstname})>"

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    queue_number = Column(Integer, nullable=False)

async def async_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)