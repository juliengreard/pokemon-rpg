def add_power(power1: str, power2: str) -> str:
    """ Adds two power strings of the form XdY """
    if not power1 or not power2 or "d" not in power1 or "d" not in power2:
        return power1  # cannot add, return first

    num1, dice1 = power1.split("d")
    num2, dice2 = power2.split("d")
    if dice1 != dice2:
        return power1  # cannot add different dice, return first

    total_num = int(num1) + int(num2)
    return f"{total_num}d{dice1}"