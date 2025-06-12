from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.config import create_db_and_tables
from src.routers import auth, cart, checkout, orders, products, users
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

app.include_router(auth.router)
app.include_router(cart.router)
app.include_router(checkout.router)
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(users.router)
