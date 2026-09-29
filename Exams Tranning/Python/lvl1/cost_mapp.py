def constellation_mapper_canvas(stars: list[tuple[int, int]],
                         size: int) -> list[str]:

    canvas: list[list] = []
    for _ in range(size):
        canvas.append(['.'] * size)

    for row, col in stars:
        if row >= 0 and row < size and col >= 0 and col < size:
            canvas[row][col] = '*'

    final_result: list = []
    for raw_list in canvas:
        final_result.append(''.join(raw_list))
    return final_result



def constellation_mapper(stars: list[tuple[int, int]],
                         size: int) -> list[str]:

    canvas: list[list] = []
    for _ in range(size):
        canvas.append(['.'] * size)

    for row, col in stars:
        if row >= 0 and row < size and col >= 0 and col < size:
            canvas[row][col] = '*'

    final_result: list = []
    for raw_list in canvas:
        final_result.append(''.join(raw_list))
    return final_result


print(f"{constellation_mapper_canvas([(0, 0), (1, 1), (2, 2)], 3)}")