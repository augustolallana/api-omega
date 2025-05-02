from typing import Union

from fastapi import FastAPI

from src.routers import admin, auth, cart, checkout, orders, products, users

app = FastAPI()

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(cart.router)
app.include_router(checkout.router)
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(users.router)
