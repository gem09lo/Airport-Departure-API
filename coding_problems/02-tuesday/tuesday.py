def duplicate_count(text: str) -> int:
    text = list(text.lower())
    text.sort()

    count = {}
    num_of_duplicates = 0
    for char in text:
        if char not in count:
            count[char] = 1
        else:
            count[char] += 1

    for v in count.values():
        if v > 1:
            num_of_duplicates += 1
    return num_of_duplicates
