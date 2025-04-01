from fastapi import FastAPI
from auth.routers import auth
from tasks import setup_periodic_tasks
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="ARES Backend")

app.include_router(auth.router, prefix="/auth", tags=["auth"])

setup_periodic_tasks(app)


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для тестирования можно разрешить все источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)