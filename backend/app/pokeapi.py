import requests


def get_best_moves(pokemon_id, level, top_n=4):
    moves = get_pokemon_moves(pokemon_id, level)
    order_moves_by_power = sorted(moves, key=lambda m: (m["power"] is not None, m["power"]), reverse=True)
    return order_moves_by_power[:top_n]

def get_pokemon_moves(pokemon_id, level):
    """
    Fetches moves available to a Pokémon up to a given level, 
    including type and power (ignores game version).
    
    Args:
        pokemon_id (int or str): Pokémon ID or name (e.g. 25 or "pikachu").
        level (int): Max level to filter moves by.

    Returns:
        List[dict]: A list of moves with name, level learned, type, and power.
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id.lower() if isinstance(pokemon_id, str) else pokemon_id}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error fetching data for {pokemon_id}: {response.status_code}")

    data = response.json()
    moves = []

    for move_entry in data["moves"]:
        move_name = move_entry["move"]["name"]
        move_url = move_entry["move"]["url"]

        # Take the minimum "level_learned_at" among version details
        level_learned = min(
            (vd["level_learned_at"] for vd in move_entry["version_group_details"] if vd["move_learn_method"]["name"] == "level-up"),
            default=None
        )

        if level_learned is not None and level_learned <= level:
            # Fetch details from the move endpoint
            move_resp = requests.get(move_url)
            if move_resp.status_code != 200:
                continue
            
            move_data = move_resp.json()
            french_name = next(
               (n["name"] for n in move_data["names"] if n["language"]["name"] == "fr"),
               move_name  # fallback to API's default (English)
            )


            short_effect = move_data["effect_entries"][0]["short_effect"] if move_data["effect_entries"] else None

            moves.append({
                "name": french_name,
                "level": level_learned,
                "type": translate_type(move_data["type"]["name"]),
                "power": transform_power_to_dices(move_data["power"]),  # can be None for status moves
                "accuracy": move_data["accuracy"],
                "effect": short_effect,
                "damage_class": move_data["damage_class"]["name"],
                "effect": move_data["effect_entries"][0]["short_effect"] if move_data["effect_entries"] else None
            })

    # Sort by level learned
    moves.sort(key=lambda m: m["level"])
    return moves

def translate_type(type, target_language="fr"):
    """
    Translates a Pokémon type to the target language using PokeAPI.
    
    Args:
        type (str): The type to translate (e.g., "fire").
        target_language (str): The target language code (default is "fr" for French).

    Returns
        str: Translated type name or original type if translation not found.
    """
    url = f"https://pokeapi.co/api/v2/type/{type.lower()}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error fetching type data for {type}: {response.status_code}")

    data = response.json()
    translated_name = next(
        (n["name"] for n in data["names"] if n["language"]["name"] == target_language),
        type  # fallback to original type if translation not found
    )

    # transform every accent to lowercase without accent
    accents = {'á': 'a', 'à': 'a', 'â': 'a', 'ä': 'a', 'ã': 'a', 'å': 'a',
               'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
               'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
               'ó': 'o', 'ò': 'o', 'ô': 'o', 'ö': 'o', 'õ': 'o',
               'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
               'ç': 'c', 'ñ': 'n'}
    for accented_char, unaccented_char in accents.items():
        translated_name = translated_name.replace(accented_char, unaccented_char)
    return translated_name

def transform_power_to_dices(power):
    """
    Transforms a move's power into a dice notation string, and reduce the power by a factor of 10.
    
    Args:
        power (int or None): The power of the move.

    Returns:
        str: Dice notation string (e.g., "2d6+3") or "0" if power is None.
    """
    if power is None:
        return ""

    power = power // 10  # Reduce power by a factor of 10
    if power <= 0:
        return ""
    
    base_dice = power // 3
    remainder = power % 3

    if base_dice == 0:
        return str(remainder)
    
    dice_str = f"{base_dice}d6"
    if remainder > 0:
        dice_str += f"+{remainder}"
    
    return dice_str
if __name__ == "__main__":

    pikachu_moves = get_pokemon_moves("pikachu", 20)
    for move in pikachu_moves:
        print(move)
