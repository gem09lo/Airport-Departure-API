def second_symbol(s: str, symbol: str) -> int:
    occurrence = 0

    for i, char in enumerate(s):
        if char == symbol:
            occurrence += 1
            if occurrence == 2:
                return i
    return -1
