from pydantic import BaseModel

# ce que le client envoie
class WildPokemonEncounter(BaseModel):
    location: str
    player_level: int = 1

class Moves(BaseModel):
    name: str
    type: str
    power: str | None = None  # peut être nul
    description: str
    status_effect: str | None = None
    status_effect_activation_chance: str | None = None 
    status_effect_deactivation_chance: str | None = None

    class Config:
        orm_mode = True

# ce qu'on renvoie (réponse)
class WildPokemon(BaseModel):
    family: str
    image: str
    types : list[str]
    level: int
    hp: int
    moves : list[Moves]

    class Config:
        orm_mode = True


class UpdateMovesRequest(BaseModel):
    pokemon1: WildPokemon
    pokemon2: WildPokemon

class UpdateMovesResponse(BaseModel):
    pokemon1: WildPokemon
    pokemon2: WildPokemon