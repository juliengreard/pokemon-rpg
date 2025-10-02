from typing import List

def get_power_for_type(current_power: str, move_type: str, opponent_types: List[str]) -> int:
    
    if not current_power:
        return current_power  # None or empty

    DOUBLE = "double"
    NO_EFFECT = "no_effect"
    DIVIDE = "divide"

    FEU = "Feu"
    EAU = "Eau"
    PLANTE = "Plante"
    ELECTRIK = "Electrik"
    GLACE = "Glace"
    NORMAL = "Normal"
    FEE = "Fee"
    COMBAT = "Combat"
    POISON = "Poison"
    SOL = "Sol"
    VOL = "Vol"
    PSY = "Psy"
    INSECT = "Insecte"
    ROCHE = "Roche"
    SPECTRE = "Spectre"
    TENEBRES = "Tenebres"
    DRAGON = "Dragon"
    ACIER = "Acier"

    effectiveness = {
        FEU: {PLANTE: DOUBLE, EAU: DIVIDE, FEU: DIVIDE, GLACE: DIVIDE, INSECT: DOUBLE, ROCHE: DIVIDE, DRAGON: DIVIDE},
        EAU: {FEU: DOUBLE, EAU: DIVIDE, PLANTE: DIVIDE, GLACE: DIVIDE, SOL: DOUBLE, DRAGON: DIVIDE},
        PLANTE: {EAU: DOUBLE, FEU: DIVIDE, PLANTE: DIVIDE, GLACE: DIVIDE, SOL: DOUBLE, VOL: DIVIDE, INSECT: DIVIDE, POISON: DIVIDE, DRAGON: DIVIDE, ACIER: DIVIDE},
        ELECTRIK: {EAU: DOUBLE, PLANTE: DIVIDE, ELECTRIK: DIVIDE, SOL: NO_EFFECT, VOL: DOUBLE, DRAGON: DIVIDE},
        GLACE: {PLANTE: DOUBLE, EAU: DOUBLE, FEU: DIVIDE, GLACE: DIVIDE, SOL: DOUBLE, VOL: DOUBLE, DRAGON: DOUBLE, ACIER: DIVIDE},
        NORMAL: {ROCHE: DIVIDE, SPECTRE: NO_EFFECT, ACIER: DIVIDE},
        FEE: {COMBAT: DOUBLE, DRAGON: DOUBLE, TENEBRES: DOUBLE, FEU: DIVIDE, POISON: DIVIDE, ACIER: DIVIDE},
        COMBAT: {NORMAL: DOUBLE, GLACE: DOUBLE, ROCHE: DOUBLE, TENEBRES: DOUBLE, ACIER: DOUBLE, POISON: DIVIDE, VOL: DIVIDE, PSY: DIVIDE, FEE: DIVIDE},
        POISON: {PLANTE: DOUBLE, FEE: DOUBLE, POISON: DIVIDE, SOL: DIVIDE, ROCHE: DIVIDE, SPECTRE: DIVIDE, ACIER: NO_EFFECT},
        SOL: {FEU: DOUBLE, ELECTRIK: DOUBLE, POISON: DOUBLE, ROCHE: DOUBLE, INSECT: DIVIDE, PLANTE: DIVIDE, VOL: NO_EFFECT},
        VOL: {PLANTE: DOUBLE, COMBAT: DOUBLE, INSECT: DOUBLE, ELECTRIK: DIVIDE, ROCHE: DIVIDE, ACIER: DIVIDE},
        PSY: {COMBAT: DOUBLE, POISON: DOUBLE, PSY: DIVIDE, TENEBRES: NO_EFFECT, ACIER: DIVIDE},
        INSECT: {PLANTE: DOUBLE, PSY: DOUBLE, TENEBRES: DOUBLE, FEU: DIVIDE, COMBAT: DIVIDE, POISON: DIVIDE, VOL: DIVIDE, ACIER: DIVIDE, FEE: DIVIDE},
        ROCHE: {FEU: DOUBLE, GLACE: DOUBLE, VOL: DOUBLE, INSECT: DOUBLE, COMBAT: DIVIDE, SOL: DIVIDE, ACIER: DIVIDE},
        SPECTRE: {PSY: DOUBLE, TENEBRES: DOUBLE, NORMAL: NO_EFFECT, COMBAT: NO_EFFECT, POISON: DIVIDE},
        TENEBRES: {PSY: DOUBLE, SPECTRE: DOUBLE, COMBAT: DIVIDE, TENEBRES: DIVIDE, FEE: DIVIDE},
        DRAGON: {DRAGON: DOUBLE, ACIER: DIVIDE, FEE: NO_EFFECT},
        ACIER: {GLACE: DOUBLE, ROCHE: DOUBLE, FEE: DOUBLE, FEU: DIVIDE, EAU: DIVIDE, ELECTRIK: DIVIDE, ACIER: DIVIDE},
    }
    
    modifier = 1.0

    for o_type in opponent_types:
        if move_type in effectiveness and o_type in effectiveness[move_type]:
            effect = effectiveness[move_type][o_type]
            if effect == DOUBLE:
                modifier *= 2
            elif effect == DIVIDE:
                modifier *= 0.5
            elif effect == NO_EFFECT:
                modifier *= 0

    current_power, dice_value = current_power.split("d") if current_power and "d" in current_power else (current_power, None)
    
    final_bonus = int(current_power) * modifier
    if final_bonus.is_integer():
        final_bonus = int(final_bonus)
    result = f"{final_bonus}d{dice_value}"


    return result
