from app import models, schemas
from app.pokeapi import get_best_moves
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.utils.dices import add_power
router = APIRouter()
from sqlalchemy import func

@router.get("/loadTeam/team1")
def load_team1(db: Session = Depends(get_db)):
    # returns 6 randoms pokemons from the DB
    # create them directly from pokemonfamilies

    pikachu = db.query(models.PokemonFamily).filter(models.PokemonFamily.name == "Pikachu").first()
    machoc = db.query(models.PokemonFamily).filter(models.PokemonFamily.name == "Machoc").first()
    dracaufeu = db.query(models.PokemonFamily).filter(models.PokemonFamily.name == "Dracaufeu").first()
    papilusion = db.query(models.PokemonFamily).filter(models.PokemonFamily.name == "Papilusion").first()
    dardargnan   = db.query(models.PokemonFamily).filter(models.PokemonFamily.name == "Dardargnan").first()
    carapuce  = db.query(models.PokemonFamily).filter(models.PokemonFamily.name == "Carapuce").first()

    tonnerre = db.query(models.BaseMove).filter(models.BaseMove.name == "tonnerre").first()
    poing_karaté = db.query(models.BaseMove).filter(models.BaseMove.name == "poing karaté").first()
    deflagration = db.query(models.BaseMove).filter(models.BaseMove.name == "deflagration").first()
    rafale_psy = db.query(models.BaseMove).filter(models.BaseMove.name == "rafale psy").first()
    furie = db.query(models.BaseMove).filter(models.BaseMove.name == "furie").first()
    pistolet_a_o = db.query(models.BaseMove).filter(models.BaseMove.name == "pistolet à o").first()

    return [
        {
            "family": pikachu.name,
            "level": 14,
            "hp": pikachu.base_hp + 14,
            "types": [t.name for t in pikachu.types],
            "image": f"/pokemon/pokemon/{pikachu.number}.png",
            "moves": [
                {
                    "name": tonnerre.name,
                    "type": tonnerre.type.name,
                    "power": tonnerre.minimal_power,
                    "description": tonnerre.description
                }
            ]
        },
                {
            "family": machoc.name,
            "level": 7,
            "hp": machoc.base_hp + 7,
            "types": [t.name for t in machoc.types],
            "image": f"/pokemon/pokemon/{machoc.number}.png",
            "moves": [
                {
                    "name": poing_karaté.name,
                    "type": poing_karaté.type.name,
                    "power": poing_karaté.minimal_power,
                    "description": poing_karaté.description
                }
            ]
        },
        {
            "family": dracaufeu.name,
            "level": 12,
            "hp": dracaufeu.base_hp + 12,
            "types": [t.name for t in dracaufeu.types],
            "image": f"/pokemon/pokemon/{dracaufeu.number}.png",
            "moves": [
                {
                    "name": deflagration.name,
                    "type": deflagration.type.name,
                    "power": deflagration.minimal_power,
                    "description": deflagration.description
                }
            ]
        },
        {
            "family": papilusion.name,
            "level": 5,
            "hp": papilusion.base_hp + 5,
            "types": [t.name for t in papilusion.types],
            "image": f"/pokemon/pokemon/{papilusion.number}.png",
            "moves": [
                {
                    "name": rafale_psy.name,
                    "type": rafale_psy.type.name,
                    "power": rafale_psy.minimal_power,
                    "description": rafale_psy.description
                }
            ]
        },
        {
            "family": dardargnan.name,
            "level": 6,
            "hp": dardargnan.base_hp + 6,
            "types": [t.name for t in dardargnan.types],
            "image": f"/pokemon/pokemon/{dardargnan.number}.png",
            "moves": [
                {
                    "name": furie.name,
                    "type": furie.type.name,
                    "power": furie.minimal_power,
                    "description": furie.description
                }
            ]
        },
        {
            "family": carapuce.name,
            "level": 4,
            "hp": carapuce.base_hp + 4,
            "types": [t.name for t in carapuce.types],
            "image": f"/pokemon/pokemon/{carapuce.number}.png",
            "moves": [
                {
                    "name": pistolet_a_o.name,
                    "type": pistolet_a_o.type.name,
                    "power": add_power(pistolet_a_o.minimal_power, "2d6"),
                    "description": pistolet_a_o.description
                }
            ]
        }

    ]

@router.get("/loadTeam/team2")
def load_team2(db: Session = Depends(get_db)):
    # returns 6 randoms pokemons from the DB
    # create them directly from pokemonfamilies

    families = db.query(models.PokemonFamily).order_by(func.random()).limit(6).all()
    team = []
    for family in families:
        level = 20  # for now fixed level
        pokemon = {
            "family": family.name,
            "level": level,
            "hp": family.base_hp + level,
            "types": [t.name for t in family.types],
            "image": f"/pokemon/pokemon/{family.number}.png",
            "moves": []

        }
        pokemon_level = 20
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
        pokemon["moves"] = moves
        team.append(pokemon)
    return team
