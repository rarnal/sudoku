from itertools import product
from timeit import time
from timer import time_deco

dico = {}

@time_deco(dico)
def sudoku_solver(puzzle):
    check_puzzle(puzzle)
    relatives = get_all_relatives()

    solve(puzzle, relatives)
    validity = valid(puzzle, relatives)

    tries = []
    if validity != 0:
        tracking = []
        if not search(puzzle, relatives, tracking, tries):
            raise ValueError("This sudoku could not be solved")
    print(len(tries))
    return puzzle


@time_deco(dico)
def check_puzzle(puzzle):
    assert len(puzzle) == 9
    assert all(len(row) == 9 for row in puzzle)
    assert all(0 <= val <= 9 for row in puzzle for val in row)


@time_deco(dico)
def print_puzzle(puzzle):
    for n in puzzle:
        print(n)


@time_deco(dico)
def search(puzzle, relatives, tracking, tries, check_tries=False):
    mini = get_min_coord(puzzle, relatives, tries, check_tries)

    if not mini:
        return False

    values, i, j = mini
    tracking.append((i, j))

    for val in values:
        puzzle[i][j] = val
        if not solve(puzzle, relatives, tracking):
            continue 
        validity = valid(puzzle, relatives)

        if validity == 0:
            return True
        elif validity == 1:
            if search(puzzle, relatives, tracking, tries, True):
                return True
        elif validity == 2: 
            clean_tracking(i, j, puzzle, tracking)
   
    clean_tracking(i, j, puzzle, tracking)
    puzzle[i][j] = 0
    tracking.pop()

    while not tracking:
        tries.append((i, j))
        if search(puzzle, relatives, tracking, tries, True):
            return True

    return False


@time_deco(dico)
def clean_tracking(i, j, puzzle, tracking):
    while tracking[-1] != (i, j):
        x, y = tracking[-1]
        puzzle[x][y] = 0
        tracking.pop()


@time_deco(dico)
def get_min_coord(puzzle, relatives, tries, check_tries):
    mini = []
    for i, j in cells():
        if puzzle[i][j] or (check_tries and (i, j) in tries):
            continue
        choice = get_choice(puzzle, relatives[i][j])
        if not mini or len(mini[0]) > len(choice):
            mini = [choice, i, j]
    return mini


@time_deco(dico)
def valid(puzzle, relatives):
    res = 0
    for i, j in cells():
        if not puzzle[i][j]:
            res = 1
        elif puzzle[i][j] in [puzzle[x][y] for x, y in relatives[i][j]]:
            return 2
    return res


@time_deco(dico)
def solve(puzzle, relatives, tracking=None):
    for i, j in cells():
        if puzzle[i][j]:
            continue
        choices = get_choice(puzzle, relatives[i][j])
        if len(choices) == 0:
            return False 
        if len(choices) == 1:
            if tracking:
                tracking.append((i, j))
            puzzle[i][j] = choices.pop()
            return solve(puzzle, relatives, tracking)
    return True


@time_deco(dico)
def get_choice(puzzle, relative):
    taken = set(puzzle[x][y] for x, y in relative)
    return [i for i in range(1, 10) if i not in taken]


@time_deco(dico)
def get_all_relatives():
    out = generate_empty_dic()
    for i, j in cells():
        out[i][j] = get_relative(i, j)
        out[i][j].discard((i, j))
    return out


@time_deco(dico)
def generate_empty_dic():
    return [[None for __ in range(9)] for _ in range(9)]


@time_deco(dico)
def get_relative(x, y):
    h = [(x, i) for i in range(9)]  #  horizontals
    v = [(i, y) for i in range(9)]  #  verticals
    x -= x%3
    y -= y%3
    d = [(x+i, y+j) for i, j in product(range(3), repeat=2)]  #  diagonals
    return set(h + v + d)


@time_deco(dico)
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
    total = 0
    with open("input.txt") as file_:
        for raw in file_:
            puzzle = parse_input(raw)
            start = time.time()
            solved = sudoku_solver(puzzle)
            end = time.time()
            print("Solved in {:0.5f} seconds".format(end-start))
            total += end - start
            print_puzzle(solved)
            print()
    print("Total time: {:0.5f} seconds".format(total))
    print(dico)

