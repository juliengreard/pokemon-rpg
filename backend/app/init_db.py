from models import Base, PokemonFamily, Pokemon
from database import engine, SessionLocal

# Création des tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Vérifie si les familles existent déjà pour éviter les doublons
if db.query(PokemonFamily).count() == 0:
    # Créer des familles
    families = [
        PokemonFamily(name="Pikachu"),
        PokemonFamily(name="Bulbizar"),
        PokemonFamily(name="Salamèche"),
        PokemonFamily(name="Carapuce")
    ]
    db.add_all(families)
    db.commit()

# Récupérer quelques familles pour associer les Pokémon
pikachu_family = db.query(PokemonFamily).filter_by(name="Pikachu").first()
bulbasaur_family = db.query(PokemonFamily).filter_by(name="Bulbasaur").first()

# Créer des Pokémon initiaux
if db.query(Pokemon).count() == 0:
    pokemons = [
        Pokemon(level=5, hp=35, family=pikachu_family),
        Pokemon(level=3, hp=45, family=bulbasaur_family)
    ]
    db.add_all(pokemons)
    db.commit()

db.close()
print("DB initialisée avec quelques Pokémon 🎉")