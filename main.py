from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import frontend, api

app = FastAPI(title="User API + UI simple")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(frontend.router)
app.include_router(api.router)
