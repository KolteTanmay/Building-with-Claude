from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from database import engine, Base
from routers import orders, gallery, admin

load_dotenv()

# Create all DB tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Crafteon Labs API",
    description="Backend for Crafteon Labs — 3D Printing Studio, Pune",
    version="1.0.0",
)

# CORS — allow your frontend origin
origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
    "http://localhost:5500",   # Live Server / VS Code
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(orders.router)
app.include_router(gallery.router)
app.include_router(admin.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Crafteon Labs API is running 🖨️"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
