# take_forge/api/v1.py
from fastapi import APIRouter
from contextlib import asynccontextmanager
from . import deps

router = APIRouter()


@asynccontextmanager
async def lifespan(app):
    deps.initialize()
    yield


@router.get("/health")
def health():
    return {"status": "ok"}
