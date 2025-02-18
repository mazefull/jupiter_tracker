import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from api.routers import all_routers


origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:5174",
    "http://localhost:5174",
]

app = FastAPI(
    title="Tracker API",
    description="Tracker API Description",
    version="0.0.1a",
)

# noinspection PyTypeChecker
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host=settings.FASTAPI_HOST, port=8000)
