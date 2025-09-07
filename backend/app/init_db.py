from models import (
    Base,
    PokemonFamily,
    Pokemon,
    Location,
    PokemonType,
    pokemonfamily_types,
    PokemonEvolution,
)

from database import (
    engine,
    SessionLocal,
)

# Création des tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# read the csv file and populate the pokemon db
# the csv file is in data/pokemon.csv
# with columns: # (number),Name,Type 1,Type 2
import csv

with open("data/pokemon_fr.csv", "r") as f:
    
    # first list of types
    types = set()
    reader = csv.DictReader(f)
    for row in reader:
        types.add(row["type"])
        if row["type2"]:
            types.add(row["type2"])
    # insert types in db if not exist
    existing_types = {t.name for t in db.query(PokemonType).all()}
    new_types = [PokemonType(name=t) for t in types if t not in existing_types]
    db.add_all(new_types)
    db.commit()

    # then insert families

    f.seek(0)
    next(f)  # skip header
    for row in reader:
        number = int(row["#"])
        name = row["pokemon"]
        type1_name = row["type"]
        type2_name = row["type2"]

        type1 = db.query(PokemonType).filter(PokemonType.name == type1_name).first()
        type2 = db.query(PokemonType).filter(PokemonType.name == type2_name).first() if type2_name else None

        print("Inserting family:", number, name, type1_name, type2_name)
        print(" type1:", type1)
        print(" type2:", type2) 
        family = db.query(PokemonFamily).filter(PokemonFamily.name == name).first()
        if not family:
            family = PokemonFamily(number=number, name=name)
            db.add(family)
            db.commit()
            db.refresh(family)
            for t in [type1, type2]:
                if t:
                    stmt = pokemonfamily_types.insert().values(family_id=family.id, type_id=t.id)
                    db.execute(stmt)
            db.commit()

    # Finally the evolutions
 
    f.seek(0)
    next(f)  # skip header
    for row in reader:
        name = row["pokemon"]
        evolution = row["evolution"]
        if evolution:
            level = 0
            pokemon_from = db.query(PokemonFamily).filter(PokemonFamily.name == name).first()
            pokemon_to = db.query(PokemonFamily).filter(PokemonFamily.name == evolution).first()
            if pokemon_from and pokemon_to:
                evolution = PokemonEvolution(
                    from_type=pokemon_from.id,
                    to_type=pokemon_to.id,
                    level=level,
                )
                db.add(evolution)
                db.commit()

db.close()
print("DB initialisée avec quelques Pokémon 🎉")

from models import BaseMove, Move
# on crée les attaques "charge", "mini-queue" et "lance_flamme"
normal_type = db.query(PokemonType).filter(PokemonType.name == "Normal").first()
fire_type = db.query(PokemonType).filter(PokemonType.name == "Feu").first()

moves = [
    BaseMove(
        name="charge",
        description="Une attaque rapide",
        minimal_power=40,
        type_id=normal_type.id,
    ),
    BaseMove(
        name="mini-queue",
        description="Une attaque de type normal",
        minimal_power=0,
        type_id=normal_type.id,
    ),
    BaseMove(
        name="lance_flamme",
        description="Une puissante attaque de feu",
        minimal_power=90,
        type_id=fire_type.id,
    ),
]
db.add_all(moves)
db.commit()