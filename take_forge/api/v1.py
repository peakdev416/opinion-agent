# take_forge/api/v1.py
from fastapi import APIRouter, Query
from contextlib import asynccontextmanager
from . import deps
from take_forge.ask_agent.ask_agent import AskAgent


router = APIRouter()
_agent = AskAgent()


@asynccontextmanager
async def lifespan(app):
    deps.initialize()
    yield


@router.get("/ask")
def ask_endpoint(q: str = Query(..., description="User question or summary request")):
    result = _agent.ask(q)
    return {"query": q, "response": result}
