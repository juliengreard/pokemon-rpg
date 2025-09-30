from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from sqlalchemy.sql.expression import func

router = APIRouter()

@router.get("/")
def list_pokemons(db: Session = Depends(get_db)):
    pokes = db.query(models.Pokemon).all()
    return [
        {"id": p.id, "family": (p.family.name if p.family else None), "level": p.level, "hp": p.hp}
        for p in pokes
    ]

@router.post("/pokemon/", response_model=schemas.WildPokemon)
def create_pokemon(data: schemas.WildPokemonEncounter, db: Session = Depends(get_db)):
    
    
    random_family = db.query(models.PokemonFamily).order_by(func.random()).first()
    family = random_family
    if not family:
        raise HTTPException(status_code=400, detail="No Pokemon family found in DB")

    # family = possible_families[0]
    print("family", family.name)
    print("types", family.types)
    
    moves = []

    from app.pokeapi import get_best_moves
    
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
    moves = get_best_moves(family.number, pokemon_level, top_n=4)
    moves = [schemas.Moves(
        name=m["name"],
        type=m["type"],
        power=str(m["power"]) if m["power"] is not None else None,
        description=m["effect"] if m["effect"] is not None else "",
        status_effect=None,
        status_effect_activation_chance=None,
        status_effect_deactivation_chance=None
    ) for m in moves]

    return schemas.WildPokemon(
        family = family.name,
        level = pokemon_level,
        hp = family.base_hp + pokemon_level,
        types = [t.name for t in family.types],
        image = f"/pokemon/pokemon/{family.number}.png",
        moves = moves
    )   
