def reverse_words(text: str) -> str:

    reversed_text = ""

    for i in text[::-1]:
        reversed_text += i

    if " " in reversed_text:
        split_text = text.split(" ")
        reversed_words = []

        for word in split_text:
            reversed_words.append(word[::-1])

        new_reversed_text = " ".join(reversed_words)
        return new_reversed_text

    return reversed_text
