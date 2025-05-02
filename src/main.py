from typing import Union

from fastapi import FastAPI

from src.routers import cart, items, login

app = FastAPI()

app.include_router(cart.router)
app.include_router(items.router)
app.include_router(login.router)
