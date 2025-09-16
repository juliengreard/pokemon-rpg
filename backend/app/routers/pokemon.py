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
    # query types of moves available for this family
    for t in family.types:
        move = db.query(models.BaseMove).filter(models.BaseMove.type == t).first()
        if move:
            attack = move.minimal_power 
            if attack != "":
                attack = move.minimal_power # add mechanism to improve power with level
            moves.append(schemas.Moves(
                name=move.name,
                type=t.name,
                power=attack,
                description=move.description,
                status_effect=move.status_effect.name if move.status_effect else None,
                status_effect_chance=30 if move.status_effect else None
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


    return schemas.WildPokemon(
        family = family.name,
        level = pokemon_level,
        hp = family.base_hp + pokemon_level,
        types = [t.name for t in family.types],
        image = f"/pokemon/pokemon/{family.number}.png",
        moves = moves
    )   
