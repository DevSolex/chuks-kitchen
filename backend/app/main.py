from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, food, cart, order, admin
from app.config import settings

app = FastAPI(title="Chuks Kitchen API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(food.router)
app.include_router(cart.router)
app.include_router(order.router)
app.include_router(admin.router)

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": "Chuks Kitchen API"}
