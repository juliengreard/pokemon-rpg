from models import (
    Base,
    PokemonFamily,
    Pokemon,
    Location,
    PokemonType,
    pokemonfamily_types,
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

with open("data/pokemon.csv", "r") as f:
    
    # first list of types
    types = set()
    reader = csv.DictReader(f)
    for row in reader:
        types.add(row["Type 1"])
        if row["Type 2"]:
            types.add(row["Type 2"])
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
        name = row["Name"]
        type1_name = row["Type 1"]
        type2_name = row["Type 2"]

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

db.close()
print("DB initialisée avec quelques Pokémon 🎉")