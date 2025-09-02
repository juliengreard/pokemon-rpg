from models import Base, PokemonFamily, Pokemon, Location
from database import engine, SessionLocal

# Création des tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

BULBI = "Bulbizarre"
# Vérifie si les familles existent déjà pour éviter les doublons
if db.query(PokemonFamily).count() == 0:
    # Créer des familles
    families = [
        PokemonFamily(name="Pikachu"),
        PokemonFamily(name=BULBI),
        PokemonFamily(name="Salamèche"),
        PokemonFamily(name="Carapuce"),
        PokemonFamily(name="Roucool"),
    ]
    db.add_all(families)
    db.commit()

# Récupérer quelques familles pour associer les Pokémon
pikachu_family = db.query(PokemonFamily).filter_by(name="Pikachu").first()
bulbasaur_family = db.query(PokemonFamily).filter_by(name=BULBI).first()
roucoul_family = db.query(PokemonFamily).filter_by(name="Roucool").first()

# Créer des Pokémon initiaux
if db.query(Pokemon).count() == 0:
    pokemons = [
        Pokemon(level=5, hp=35, family=pikachu_family),
        Pokemon(level=3, hp=45, family=bulbasaur_family)
    ]
    db.add_all(pokemons)
    db.commit()

# Créer des emplacements initiaux
if db.query(Location).count() == 0:
    locations = [
        Location(name="grass"),
        Location(name="water"),
        Location(name="cave"),
    ]
    db.add_all(locations)
    db.commit()

# retrieve families and location once after everything is added to session
bulbizarre_family = db.query(PokemonFamily).filter_by(name=BULBI).first()
roucoul_family = db.query(PokemonFamily).filter_by(name="Roucool").first()
grass_location = db.query(Location).filter_by(name="grass").first()

# append families
for family in [bulbizarre_family, roucoul_family]:
    print(f"Adding family {family.name} to location {grass_location.name}")
    if family not in grass_location.families:
        grass_location.families.append(family)

# commit all changes at once
db.commit()

db.close()
print("DB initialisée avec quelques Pokémon 🎉")