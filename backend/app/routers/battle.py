from fastapi import APIRouter
from schemas import UpdateMovesRequest, UpdateMovesResponse
from schemas import Moves
from utils.power import get_power_for_type

router = APIRouter()

@router.post("/battle/update_moves", response_model=UpdateMovesResponse)
def update_moves(req: UpdateMovesRequest):
    
    returned_pokemon1 = req.pokemon1
    returned_pokemon2 = req.pokemon2

    print("updating move 1")
    # ⚡ Here you implement logic, e.g. adjust power depending on opponent type
    updated_moves1 = []
    print("Current moves:", req.pokemon1.moves)
    for move in req.pokemon1.moves:
        print("Updating move:", move.name)
        new_power = move.power or 0
        # Example: bonus if type matches
        new_power = get_power_for_type(move.power, move.type, req.pokemon2.types)
        updated_moves1.append(Moves(
            name=move.name,
            type=move.type,
            power=new_power,
            description=move.description
        ))
    returned_pokemon1.moves = updated_moves1
    print("Updated moves:", returned_pokemon1.moves)

    updated_moves2 = []
    for move in req.pokemon2.moves:
        new_power = move.power or 0
        
        new_power = get_power_for_type(move.power, move.type, req.pokemon1.types)
        updated_moves2.append(Moves(
            name=move.name,
            type=move.type,
            power=new_power,
            description=move.description
        ))
    returned_pokemon2.moves = updated_moves2
    print("Updated moves:", returned_pokemon2.moves)

    return UpdateMovesResponse(pokemon1=returned_pokemon1, pokemon2=returned_pokemon2)