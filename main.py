from fastapi import FastAPI

from api.routes import router

app = FastAPI(
    title="Research Paper Discovery & Summarization Agent",
    version="1.0.0"
)

app.include_router(router)