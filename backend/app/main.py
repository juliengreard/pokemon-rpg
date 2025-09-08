from fastapi import (
    FastAPI,
    Depends, 
    HTTPException, 
    Query,
)
from sqlalchemy.orm import Session

from app.database import (
    SessionLocal,
    engine,
)
from app import (
    models,
    schema,
)
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# app = FastAPI()


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
models.Base.metadata.create_all(bind=engine)

# dépendance DB par requête
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "ok"}


# Liste tous les pokémon (avec nom de famille)
@app.get("/pokemons")
def list_pokemons(db: Session = Depends(get_db)):
    pokes = db.query(models.Pokemon).all()
    return [
        {"id": p.id, "family": (p.family.name if p.family else None), "level": p.level, "hp": p.hp}
        for p in pokes
    ]

@app.post("/pokemon/", response_model=schema.WildPokemon)
def create_pokemon(data: schema.WildPokemonEncounter, db: Session = Depends(get_db)):
    
    from sqlalchemy.sql.expression import func
    
    random_family = db.query(models.PokemonFamily).order_by(func.random()).first()
    family = random_family
    if not family:
        raise HTTPException(status_code=400, detail="No Pokemon family found in DB")

    # # find families from the given location
    # location = db.query(models.Location).filter(models.Location.name == data.location).first()
    # if not location:
    #     raise HTTPException(status_code=400, detail="Location not found")
    # possible_families = location.families
    # if not possible_families:
    #     raise HTTPException(status_code=400, detail="No Pokemon families found in this location")
    
    # family = possible_families[0]
    print("family", family.name)
    print("types", family.types)
    
    moves = []
    # query types of moves available for this family
    for t in family.types:
        move = db.query(models.BaseMove).filter(models.BaseMove.type == t).first()
        if move:
            attack = move.minimal_power 
            if attack > 0:
                attack = move.minimal_power + (data.player_level - 1) * 10
            moves.append(schema.Moves(
                name=move.name,
                type=t.name,
                power=attack,
                description=move.description
            ))
    return schema.WildPokemon(
        family=family.name,
        level=data.player_level,
        hp=100,
        types = [t.name for t in family.types],
        image = f"/pokemon/pokemon/{family.number}.png",
        moves = moves
    )   





from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from app.schema import WildPokemon, Moves


class UpdateMovesRequest(BaseModel):
    pokemon1: WildPokemon
    pokemon2: WildPokemon

class UpdateMovesResponse(BaseModel):
    pokemon1: WildPokemon
    pokemon2: WildPokemon

@app.post("/battle/update_moves", response_model=UpdateMovesResponse)
def update_moves(req: UpdateMovesRequest):
    
    returned_pokemon1 = req.pokemon1
    returned_pokemon2 = req.pokemon2

    print("updating move 1")
    # ⚡ Here you implement logic, e.g. adjust power depending on opponent type
    updated_moves = []
    print("Current moves:", req.pokemon1.moves)
    for move in req.pokemon1.moves:
        print("Updating move:", move.name)
        new_power = move.power or 0
        # Example: bonus if type matches
        if move.type in req.pokemon2.types:
            new_power += 10
        updated_moves.append(Moves(
            name=move.name,
            type=move.type,
            power=new_power,
            description=move.description
        ))
    returned_pokemon1.moves = updated_moves
    print("Updated moves:", returned_pokemon1.moves)

    for move in req.pokemon2.moves:
        new_power = move.power or 0
        if move.type in req.pokemon1.types:
            new_power += 10
        updated_moves.append(Moves(
            name=move.name,
            type=move.type,
            power=new_power,
            description=move.description
        ))
    returned_pokemon2.moves = updated_moves
    print("Updated moves:", returned_pokemon2.moves)

    return UpdateMovesResponse(pokemon1=returned_pokemon1, pokemon2=returned_pokemon2)