from itertools import product, permutations


def sudoku_solver(puzzle):

    relatives = get_all_relatives()
    solve(puzzle, relatives)
    validity = valid(puzzle, relatives)
    if validity != 0:
        tracking = []
        tries = []
        search(puzzle, relatives, tracking, tries)
    return puzzle


def print_puzzle(puzzle):
    for n in puzzle:
        print(n)


def search(puzzle, relatives, tracking, tries):
    values, i, j = get_min_coord(puzzle, relatives, tries)
    tracking.append((i, j))

    for val in values:
        puzzle[i][j] = val
        solve(puzzle, relatives, tracking)
        validity = valid(puzzle, relatives)

        if validity == 0:
            return True
        if validity == 1:
            if search(puzzle, relatives, tracking, tries):
                return True

    while tracking[-1] != (i, j):
        x, y = tracking[-1]
        puzzle[x][y] = 0
        del tracking[-1]

    puzzle[i][j] = 0
    del tracking[-1]

    while not tracking:
        tries.append((i, j))
        if search(puzzle, relatives, tracking, tries):
            return True

    return False


def get_min_coord(puzzle, relatives, tries):
    mini = []
    for i, j in cells():
        if puzzle[i][j] or (i, j) in tries:
            continue
        choice = get_choice(puzzle, relatives[i][j])
        if not mini or len(mini[0]) > len(choice):
            mini = [choice, i, j]
    if not mini:
        print_puzzle(puzzle)
    return mini


def valid(puzzle, relatives):
    res = 0
    for i, j in cells():
        if not puzzle[i][j]:
            res = 1
        elif puzzle[i][j] in [puzzle[x][y] for x, y in relatives[i][j]]:
            return 2
    return res


def solve(puzzle, relatives, tracking=None):
    for i, j in cells():
        if puzzle[i][j]:
            continue
        choices = get_choice(puzzle, relatives[i][j])
        if len(choices) == 1:
            if tracking:
                tracking.append((i, j))
            puzzle[i][j] = choices.pop()
            solve(puzzle, relatives, tracking)


def get_choice(puzzle, relative):
    taken = set(puzzle[x][y] for x, y in relative)
    return [i for i in range(1, 10) if i not in taken]


def get_all_relatives():
    out = generate_empty_dic()
    for i, j in cells():
        out[i][j] = get_relative(i, j)
        out[i][j].discard((i, j))
    return out


def generate_empty_dic():
    return [[None for __ in range(9)] for _ in range(9)]


def get_relative(x, y):
    h = [(x, i) for i in range(9)]  # horizontals
    v = [(i, y) for i in range(9)]  # verticals
    x -= x % 3
    y -= y % 3
    d = [(x+i, y+j) for i, j in product(range(3), repeat=2)]  # diagonals
    return set(h + v + d)


def cells():
    for i, j in product(range(9), repeat=2):
        yield (i, j)


def copy(puzzle):
    out = generate_empty_dic()
    for i, j in cells():
        out[i][j] = puzzle[i][j]
    return out


def parse_input(raw):
    raw = raw[:-1]
    assert len(raw) == 9*9
    assert raw.isdigit()

    out = generate_empty_dic()
    for i, j in product(range(9), repeat=2):
        out[i][j] = int(raw[i*9+j])
    return out


if __name__ == "__main__":
    with open("input.txt") as _file:
        raw = _file.readline()
        puzzle = parse_input(raw)
        solved = sudoku_solver(puzzle)
        print_puzzle(solved)
        print()
