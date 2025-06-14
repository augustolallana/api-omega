from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.config import create_db_and_tables
from src.routers import auth, users
from src.routers.cart import cart
from src.routers.order import checkout, orders
from src.routers.product import (
    brand,
    category,
    image,
    products,
    promotion,
    tag,
)
from src.settings import settings


# Runs on every server startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for the FastAPI application."""
    create_db_and_tables()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"/{settings.API_BASE_PATH}/openapi.json",
    lifespan=lifespan,
)

# Auth and user routes
app.include_router(auth.router)
app.include_router(users.router)

# Cart routes
app.include_router(cart.router)

# Order routes
app.include_router(checkout.router)
app.include_router(orders.router)

# Product routes
app.include_router(products.router)
app.include_router(brand.router)
app.include_router(category.router)
app.include_router(promotion.router)
app.include_router(tag.router)
app.include_router(image.router)
