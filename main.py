import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
from take_forge.api import v1
from take_forge.api.v1 import lifespan



def get_application():
    _app = FastAPI(title="TakeForge", lifespan=lifespan)

    # Add middlewares here

    _app.include_router(v1.router, prefix="/api/v1")
    return _app


app = get_application()


def main():
    env = os.getenv("ENV", "development")
    port = int(os.getenv("PORT", "8080"))
    workers = int(os.getenv("WORKERS", "1"))

    uvicorn.run(
        "main:app",
        port=port,
        host="0.0.0.0",
        reload=(env == "development"),
        workers=workers,
        use_colors=False,
    )


if __name__ == "__main__":
    main()
