def cleaned_counts(data: list[int]) -> list[int]:
    copy_data = data[:]
    ordered_data = sorted(data)

    if copy_data == ordered_data:
        return copy_data
    for number in range(len(copy_data) - 1):
        current_idx = number
        next_idx = number + 1

        if copy_data[current_idx] > copy_data[next_idx]:
            copy_data[next_idx] = copy_data[current_idx]
    return copy_data
