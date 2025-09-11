from fastapi import (
    FastAPI,
    Depends, 
    HTTPException, 
    Query,
)
from app.database import (
    SessionLocal,
    engine,
)
from app import (
    models,
    schema,
)
import os

from pydantic import BaseModel
from typing import List, Optional
from app.schema import WildPokemon, Moves
from sqlalchemy.orm import Session

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()



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
            if attack != "":
                attack = move.minimal_power # add mechanism to improve power with level
            moves.append(schema.Moves(
                name=move.name,
                type=t.name,
                power=attack,
                description=move.description
            ))

    
    def compute_level(player_level: int) -> int:
        import random
        # Pokémon level is between player_level 1 and 100, gaussian distribution around player_level
        level = int(random.gauss(player_level, 5))
        if level < 1:
            level = 1
        if level > 100:
            level = 100
        return level
    
    pokemon_level = compute_level(data.player_level)


    return schema.WildPokemon(
        family = family.name,
        level = pokemon_level,
        hp = family.base_hp + pokemon_level,
        types = [t.name for t in family.types],
        image = f"/pokemon/pokemon/{family.number}.png",
        moves = moves
    )   

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
    updated_moves1 = []
    print("Current moves:", req.pokemon1.moves)
    for move in req.pokemon1.moves:
        print("Updating move:", move.name)
        new_power = move.power or 0
        # Example: bonus if type matches
        new_power = get_power_for_type(move.power, move.type, req.pokemon2.types)
        updated_moves1.append(Moves(
            name=move.name,
            type=move.type,
            power=new_power,
            description=move.description
        ))
    returned_pokemon1.moves = updated_moves1
    print("Updated moves:", returned_pokemon1.moves)

    updated_moves2 = []
    for move in req.pokemon2.moves:
        new_power = move.power or 0
        
        new_power = get_power_for_type(move.power, move.type, req.pokemon1.types)
        updated_moves2.append(Moves(
            name=move.name,
            type=move.type,
            power=new_power,
            description=move.description
        ))
    returned_pokemon2.moves = updated_moves2
    print("Updated moves:", returned_pokemon2.moves)

    return UpdateMovesResponse(pokemon1=returned_pokemon1, pokemon2=returned_pokemon2)

def get_power_for_type(current_power: str, move_type: str, opponent_types: List[str]) -> int:
    
    DOUBLE = "double"
    NO_EFFECT = "no_effect"
    DIVIDE = "divide"

    FEU = "Feu"
    EAU = "Eau"
    PLANTE = "Plante"
    ELECTRIK = "Electrik"
    GLACE = "Glace"
    NORMAL = "Normal"
    FEE = "Fee"
    COMBAT = "Combat"
    POISON = "Poison"
    SOL = "Sol"
    VOL = "Vol"
    PSY = "Psy"
    INSECT = "Insecte"
    ROCHE = "Roche"
    SPECTRE = "Spectre"
    TENEBRES = "Tenebres"
    DRAGON = "Dragon"
    ACIER = "Acier"

    effectiveness = {
        FEU: {PLANTE: DOUBLE, EAU: DIVIDE, FEU: DIVIDE, GLACE: DIVIDE, INSECT: DOUBLE, ROCHE: DIVIDE, DRAGON: DIVIDE},
        EAU: {FEU: DOUBLE, EAU: DIVIDE, PLANTE: DIVIDE, GLACE: DIVIDE, SOL: DOUBLE, DRAGON: DIVIDE},
        PLANTE: {EAU: DOUBLE, FEU: DIVIDE, PLANTE: DIVIDE, GLACE: DIVIDE, SOL: DOUBLE, VOL: DIVIDE, INSECT: DIVIDE, POISON: DIVIDE, DRAGON: DIVIDE, ACIER: DIVIDE},
        ELECTRIK: {EAU: DOUBLE, PLANTE: DIVIDE, ELECTRIK: DIVIDE, SOL: NO_EFFECT, VOL: DOUBLE, DRAGON: DIVIDE},
        GLACE: {PLANTE: DOUBLE, EAU: DOUBLE, FEU: DIVIDE, GLACE: DIVIDE, SOL: DOUBLE, VOL: DOUBLE, DRAGON: DOUBLE, ACIER: DIVIDE},
        NORMAL: {ROCHE: DIVIDE, SPECTRE: NO_EFFECT, ACIER: DIVIDE},
        FEE: {COMBAT: DOUBLE, DRAGON: DOUBLE, TENEBRES: DOUBLE, FEU: DIVIDE, POISON: DIVIDE, ACIER: DIVIDE},
        COMBAT: {NORMAL: DOUBLE, GLACE: DOUBLE, ROCHE: DOUBLE, TENEBRES: DOUBLE, ACIER: DOUBLE, POISON: DIVIDE, VOL: DIVIDE, PSY: DIVIDE, FEE: DIVIDE},
        POISON: {PLANTE: DOUBLE, FEE: DOUBLE, POISON: DIVIDE, SOL: DIVIDE, ROCHE: DIVIDE, SPECTRE: DIVIDE, ACIER: NO_EFFECT},
        SOL: {FEU: DOUBLE, ELECTRIK: DOUBLE, POISON: DOUBLE, ROCHE: DOUBLE, INSECT: DIVIDE, PLANTE: DIVIDE, VOL: NO_EFFECT},
        VOL: {PLANTE: DOUBLE, COMBAT: DOUBLE, INSECT: DOUBLE, ELECTRIK: DIVIDE, ROCHE: DIVIDE, ACIER: DIVIDE},
        PSY: {COMBAT: DOUBLE, POISON: DOUBLE, PSY: DIVIDE, TENEBRES: NO_EFFECT, ACIER: DIVIDE},
        INSECT: {PLANTE: DOUBLE, PSY: DOUBLE, TENEBRES: DOUBLE, FEU: DIVIDE, COMBAT: DIVIDE, POISON: DIVIDE, VOL: DIVIDE, ACIER: DIVIDE, FEE: DIVIDE},
        ROCHE: {FEU: DOUBLE, GLACE: DOUBLE, VOL: DOUBLE, INSECT: DOUBLE, COMBAT: DIVIDE, SOL: DIVIDE, ACIER: DIVIDE},
        SPECTRE: {PSY: DOUBLE, TENEBRES: DOUBLE, NORMAL: NO_EFFECT, COMBAT: NO_EFFECT, POISON: DIVIDE},
        TENEBRES: {PSY: DOUBLE, SPECTRE: DOUBLE, COMBAT: DIVIDE, TENEBRES: DIVIDE, FEE: DIVIDE},
        DRAGON: {DRAGON: DOUBLE, ACIER: DIVIDE, FEE: NO_EFFECT},
        ACIER: {GLACE: DOUBLE, ROCHE: DOUBLE, FEE: DOUBLE, FEU: DIVIDE, EAU: DIVIDE, ELECTRIK: DIVIDE, ACIER: DIVIDE},
    }
    
    modifier = 1

    print("Calculating power for move type", move_type, "against opponent types", opponent_types)
    print("Current power:", current_power)
    for o_type in opponent_types:
        if move_type in effectiveness and o_type in effectiveness[move_type]:
            effect = effectiveness[move_type][o_type]
            if effect == DOUBLE:
                modifier *= 2
            elif effect == DIVIDE:
                modifier *= 0.5
            elif effect == NO_EFFECT:
                modifier *= 0

    current_power, dice_value = current_power.split("d") if current_power and "d" in current_power else (current_power, None)
    result = f"{int(current_power) * modifier}d{dice_value}"
    print("New power:", result)
    return result