def missing(nums: list[int], s: str) -> str:
    answer = ""

    ordered_nums = sorted(nums)
    new_s = s.replace(" ", "").lower()

    if ordered_nums[-1] >= len(new_s):
        return "No mission today"
    else:
        for i in ordered_nums:
            answer += new_s[i]
    return answer
