from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from config.config import get_config

from models.user import User  # noqa
from models.product import Product  # noqa
from models.product_image import ProductImage  # noqa
from models.category import Category  # noqa
from models.company import Company  # noqa
from models.address import Address  # noqa
from models.cart import Cart  # noqa
from models.cart_product import CartProduct  # noqa
from models.order import Order  # noqa
from models.order_item import OrderItem  # noqa
from models.token import Token  # noqa


CONFIG = get_config()

USER = CONFIG.POSTGRES_USER
PASSWORD = CONFIG.POSTGRES_PASSWORD
HOST = CONFIG.POSTGRES_HOST
PORT = CONFIG.POSTGRES_PORT
DB = CONFIG.POSTGRES_DB


DATABASE_URL = f"postgresql+psycopg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"


engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    return async_session


async def init_models():
    from models.base import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
