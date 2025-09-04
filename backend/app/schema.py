from pydantic import BaseModel

# ce que le client envoie
class WildPokemonEncounter(BaseModel):
    location: str
    player_level: int = 1

# ce qu'on renvoie (réponse)
class WildPokemon(BaseModel):
    family: str
    image: str
    types : list[str]
    level: int
    hp: int

    class Config:
        orm_mode = True
