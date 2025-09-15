from fastapi import (
    FastAPI,
)
import os
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


from app.models import BaseMove, Move, Base

from app.database import (
    engine,
)

from app.schemas import WildPokemon, Moves
from app.routers import pokemon, team, battle


app = FastAPI(title="Pokemon RPG API")

# --- CORS middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev only, later you can restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
BASE_DIR = "/app"  # container working dir
IMAGES_DIR = os.path.join(BASE_DIR, "data/images")

app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")

# crée les tables si besoin
Base.metadata.create_all(bind=engine)


app.include_router(pokemon.router, prefix="", tags=["pokemon"])
app.include_router(team.router, prefix="", tags=["teams"])
app.include_router(battle.router, prefix="", tags=["battle"])

@app.get("/")
def root():
    return {"status": "ok"}


