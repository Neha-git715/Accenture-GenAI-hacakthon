 # Main FastAPI app

from fastapi import FastAPI
from api.endpoints import router
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="BankGen360", version="1.0")
app.include_router(router, prefix="/api")
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def health_check():
    return {"status": "active", "service": "Customer 360 Designer"}