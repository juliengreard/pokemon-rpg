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

spectre_type = db.query(PokemonType).filter(PokemonType.name == "Spectre").first()
ice_type = db.query(PokemonType).filter(PokemonType.name == "Glace").first()
fairy_type = db.query(PokemonType).filter(PokemonType.name == "Fee").first()
normal_type = db.query(PokemonType).filter(PokemonType.name == "Normal").first()
fire_type = db.query(PokemonType).filter(PokemonType.name == "Feu").first()
combat_type = db.query(PokemonType).filter(PokemonType.name == "Combat").first()
grass_type = db.query(PokemonType).filter(PokemonType.name == "Plante").first()
water_type = db.query(PokemonType).filter(PokemonType.name == "Eau").first()
electric_type = db.query(PokemonType).filter(PokemonType.name == "Electrik").first()
flying_type = db.query(PokemonType).filter(PokemonType.name == "Vol").first()
rock_type = db.query(PokemonType).filter(PokemonType.name == "Roche").first()
ground_type = db.query(PokemonType).filter(PokemonType.name == "Sol").first()
poison_type = db.query(PokemonType).filter(PokemonType.name == "Poison").first()
bug_type = db.query(PokemonType).filter(PokemonType.name == "Insecte").first()
psychic_type = db.query(PokemonType).filter(PokemonType.name == "Psy").first()
dragon_type = db.query(PokemonType).filter(PokemonType.name == "Dragon").first()
dark_type = db.query(PokemonType).filter(PokemonType.name == "Tenebres").first()
steel_type = db.query(PokemonType).filter(PokemonType.name == "Acier").first()




default_moves = [
    BaseMove(
        name="charge",
        description="Une attaque rapide",
        minimal_power=40,
        type_id=normal_type.id,
    ),
    BaseMove(
        name="lance flamme",
        description="Une puissante attaque de feu",
        minimal_power=90,
        type_id=fire_type.id,
    ),
    BaseMove(
        name="pistolet à eau",
        description="Une attaque d'eau",
        minimal_power=40,
        type_id=water_type.id,
    ),
    BaseMove(
        name="éclair",
        description="Une attaque électrique",
        minimal_power=40,
        type_id=electric_type.id,
    ),
    BaseMove(
        name="laser glace",
        description="Une attaque de glace",
        minimal_power=90,
        type_id=ice_type.id,
    ),
    BaseMove(
        name="vent violent",
        description="Une attaque de type vol",
        minimal_power=90,
        type_id=flying_type.id,
    ),
    BaseMove(
        name="piqûre",
        description="Une attaque de type insecte",
        minimal_power=40,
        type_id=bug_type.id,
    ),
    BaseMove(
        name="poudre toxik",
        description="Une attaque de type poison",
        minimal_power=90,
        type_id=poison_type.id,
    ),
    BaseMove(
        name="lame de roc",
        description="Une attaque de type roche",
        minimal_power=90,
        type_id=rock_type.id,
    ),
    BaseMove(
        name="séisme",
        description="Une attaque de type sol",
        minimal_power=90,
        type_id=ground_type.id,
    ),
    BaseMove(
        name="fouet lianes",
        description="Une attaque de type plante",
        minimal_power=90,
        type_id=grass_type.id,
    ),
    BaseMove(
        name="psyko",
        description="Une attaque de type psy",
        minimal_power=90,
        type_id=psychic_type.id,
    ),
    BaseMove(
        name="draco-queue",
        description="Une attaque de type dragon",
        minimal_power=90,
        type_id=dragon_type.id,
    ),
    BaseMove(
        name="tranche nuit",
        description="Une attaque de type ténèbres",
        minimal_power=90,
        type_id=dark_type.id,
    ),
    BaseMove(
        name="lame d'acier",
        description="Une attaque de type acier",
        minimal_power=90,
        type_id=steel_type.id,
    ),
    BaseMove(
        name="ball'ombre",
        description="Une attaque de type spectre",
        minimal_power=90,
        type_id=spectre_type.id,
    ),
    BaseMove(
        name="choc mental",
        description="Une attaque de type fée",
        minimal_power=90,
        type_id=fairy_type.id,
    ), 
    BaseMove(
        name="force",
        description="Une attaque de type combat",
        minimal_power=90,
        type_id=combat_type.id,
    ),
]
db.add_all(default_moves)
db.commit()