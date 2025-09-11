import os
import shutil

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
from typing import Tuple

def get_regional_name_and_id(id : int, french_name : str) -> Tuple[int, str]:
    
    mapping = {
        "19":  { "Alola" : "Alolan Rattata", },
        "20":  { "Alola" : "Alolan Raticate", },
        "26":  { "Alola" : "Alolan Raichu", },
        "27":  { "Alola" : "Alolan Sandshrew", },
        "28":  { "Alola" : "Alolan Sandslash", },
        "37":  { "Alola" : "Alolan Vulpix", },
        "38":  { "Alola" : "Alolan Ninetales", },
        "50":  { "Alola" : "Alolan Diglett", },
        "51":  { "Alola" : "Alolan Dugtrio", },
        "52":  { "Galar" : "Galarian Meowth", "Alola" : "Alolan Meowth"},
        "53":  { "Alola" : "Alolan Persian", },
        "58":  { "Hisui" : "Hisuian Growlithe", },
        "59":  { "Hisui" : "Hisuian Arcanine", },
        "74":  { "Alola" : "Alolan Geodude", },
        "75":  { "Alola" : "Alolan Graveler", },
        "76":  { "Alola" : "Alolan Golem", },
        "77":  { "Galar" : "Galarian Ponyta", },
        "78":  { "Galar" : "Galarian Rapidash", },
        "79":  { "Galar" : "Galarian Slowpoke", },
        "80":  { "Galar" : "Galarian Slowbro", },
        "83":  { "Galar" : "Galarian Farfetch’d", },
        "88":  { "Alola" : "Alolan Grimer", },
        "89":  { "Alola" : "Alolan Muk", },
        "100": { "Hisui" : "Hisuian Voltorb", },
        "101": { "Hisui" : "Hisuian Electrode", },
        "103": { "Alola" : "Alolan Exeggutor", },
        "105": { "Alola" : "Alolan Marowak", },
        "110": { "Galar" : "Galarian Weezing", },
        "122": { "Galar" : "Galarian Mr. Mime", },
        "144": { "Galar" : "Galarian Articuno", },
        "145": { "Galar" : "Galarian Zapdos", },
        "146": { "Galar" : "Galarian Moltres", },
    }

    bonus_ids = {
        "Alola": 5000,
        "Galar": 6000,
        "Hisui": 7000,
    }
    english_name = french_name
    new_id = id
    for key in bonus_ids:
        if key in french_name:
            new_id = int(id) + bonus_ids[key]
            break
    str_id = str(id)
    if str_id in mapping:
        for key in mapping[str_id]:
            if key in french_name:
                english_name = mapping[str_id][key]

    print(f"Warning: no english name for {new_id} {french_name}")

    return (new_id, english_name)

hps = {}
with open("data/pokemon_en.csv", "r") as f:
    # f.seek(0)
    # next(f)  # skip header
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
        number = int(row["#"])
        hps[number] = int(row["PV"])

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
        hp = hps.get(number, 15)
        # on divise hp par 3 pour avoir des pv liés à la mécanique de d6
        hp = hp // 6

        type1 = db.query(PokemonType).filter(PokemonType.name == type1_name).first()
        type2 = db.query(PokemonType).filter(PokemonType.name == type2_name).first() if type2_name else None
        
        # if number alreaydy in db, print name and skip
        family = db.query(PokemonFamily).filter(PokemonFamily.number == number).first()
        if family:
            print(f"[{number}] {name}")
            new_id, folder_name = get_regional_name_and_id(number, name)
            if new_id != number:
                print(f"  -> {new_id} {folder_name}")
                family_regional = db.query(PokemonFamily).filter(PokemonFamily.number == new_id).first()
                if not family_regional:
                    family_regional = PokemonFamily(number=new_id, name=name, base_hp = hp)
                    db.add(family_regional)
                    db.commit()
                    db.refresh(family_regional)
                    for t in [type1, type2]:
                        if t:
                            stmt = pokemonfamily_types.insert().values(family_id=family_regional.id, type_id=t.id)
                            db.execute(stmt)
                    db.commit()
                    # after creating the family, save the image associated

                    folder = f"data/images/english/{folder_name}"
                    if os.path.exists(folder):
                        # find the image .png with "_new" in this folder and copy
                        # it to images/pokemon/pokemon/{new_id}.png
                        for file in os.listdir(folder):
                            if file.endswith(".png") and "_new" in file:
                                src = os.path.join(folder, file)
                                dst = f"data/images/pokemon/pokemon/{new_id}.png"
                                shutil.copyfile(src, dst)
                                print(f"  -> copied image {src} to {dst}")
                                break

            continue
        if not family:
            family = PokemonFamily(number=number, name=name, base_hp=hp)
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
        minimal_power="1d6",
        type_id=normal_type.id,
    ),
    BaseMove(
        name="lance flamme",
        description="Une puissante attaque de feu",
        minimal_power="1d6",
        type_id=fire_type.id,
    ),
    BaseMove(
        name="pistolet à eau",
        description="Une attaque d'eau",
        minimal_power="1d6",
        type_id=water_type.id,
    ),
    BaseMove(
        name="éclair",
        description="Une attaque électrique",
        minimal_power="1d6",
        type_id=electric_type.id,
    ),
    BaseMove(
        name="laser glace",
        description="Une attaque de glace",
        minimal_power="1d6",
        type_id=ice_type.id,
    ),
    BaseMove(
        name="vent violent",
        description="Une attaque de type vol",
        minimal_power="1d6",
        type_id=flying_type.id,
    ),
    BaseMove(
        name="piqûre",
        description="Une attaque de type insecte",
        minimal_power="1d6",
        type_id=bug_type.id,
    ),
    BaseMove(
        name="poudre toxik",
        description="Une attaque de type poison",
        minimal_power="1d6",
        type_id=poison_type.id,
    ),
    BaseMove(
        name="lame de roc",
        description="Une attaque de type roche",
        minimal_power="1d6",
        type_id=rock_type.id,
    ),
    BaseMove(
        name="séisme",
        description="Une attaque de type sol",
        minimal_power="1d6",
        type_id=ground_type.id,
    ),
    BaseMove(
        name="fouet lianes",
        description="Une attaque de type plante",
        minimal_power="1d6",
        type_id=grass_type.id,
    ),
    BaseMove(
        name="psyko",
        description="Une attaque de type psy",
        minimal_power="1d6",
        type_id=psychic_type.id,
    ),
    BaseMove(
        name="draco-queue",
        description="Une attaque de type dragon",
        minimal_power="1d6",
        type_id=dragon_type.id,
    ),
    BaseMove(
        name="tranche nuit",
        description="Une attaque de type ténèbres",
        minimal_power="1d6",
        type_id=dark_type.id,
    ),
    BaseMove(
        name="lame d'acier",
        description="Une attaque de type acier",
        minimal_power="1d6",
        type_id=steel_type.id,
    ),
    BaseMove(
        name="ball'ombre",
        description="Une attaque de type spectre",
        minimal_power="1d6",
        type_id=spectre_type.id,
    ),
    BaseMove(
        name="choc mental",
        description="Une attaque de type fée",
        minimal_power="1d6",
        type_id=fairy_type.id,
    ), 
    BaseMove(
        name="force",
        description="Une attaque de type combat",
        minimal_power="1d6",
        type_id=combat_type.id,
    ),
]
db.add_all(default_moves)
db.commit()