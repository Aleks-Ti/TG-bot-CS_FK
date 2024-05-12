async def hint_number(numbers: list[int], target: int) -> str:
    nearest_lower = 0
    nearest_higher = 100
    numbers.sort()
    for num in numbers:
        if nearest_lower < num <= target:
            nearest_lower = num
            continue
        if nearest_higher > num > target:
            nearest_higher = num
            break

    return str((nearest_higher - nearest_lower) // 2 + nearest_lower)
