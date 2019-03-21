from itertools import product


def sudoku_solver(puzzle):
    print_puzzle(puzzle)
    check_puzzle(puzzle)
    relatives = get_all_relatives()
    solve(puzzle, relatives)
    validity = valid(puzzle, relatives)
    tracking = []
    tries = []

    if validity != 0:
        if not search(puzzle, relatives, tracking, tries):
            raise ValueError("This sudoku could not be solved")
    print(len(tries))
    return puzzle


def check_puzzle(puzzle):
    assert len(puzzle) == 9
    assert all(len(row) == 9 for row in puzzle)
    assert all(0 <= val <= 9 for row in puzzle for val in row)


def print_puzzle(puzzle):
    for n in puzzle:
        print(n)


def search(puzzle, relatives, tracking, tries, check_tries=False, count=0):
    mini = get_min_coord(puzzle, relatives, tries, check_tries)

    if not mini:
        return False

    values, i, j = mini
    tracking.append((i, j))

    #print("{}{}".format(' '*count, (i, j)))
    count += 1

    for val in values:
        puzzle[i][j] = val
        if not solve(puzzle, relatives, tracking):
            break 
        validity = valid(puzzle, relatives)

        if validity == 0:
            return True
        elif validity == 1:
            if search(puzzle, relatives, tracking, tries, count):
                return True
        elif validity == 2: 
            clean_tracking(i, j, puzzle, tracking)
   
    clean_tracking(i, j, puzzle, tracking)
    puzzle[i][j] = 0
    del tracking[-1]

    while not tracking:
        tries.append((i, j))
        if search(puzzle, relatives, tracking, tries, True, count):
            return True

    return False


def clean_tracking(i, j, puzzle, tracking):
    while tracking[-1] != (i, j):
        x, y = tracking[-1]
        puzzle[x][y] = 0
        del tracking[-1]


def get_min_coord(puzzle, relatives, tries, check_tries):
    mini = []
    for i, j in cells():
        if puzzle[i][j] or (check_tries and (i, j) in tries):
            continue
        choice = get_choice(puzzle, relatives[i][j])
        if not mini or len(mini[0]) > len(choice):
            mini = [choice, i, j]
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
        if len(choices) == 0:
            return False 
        if len(choices) == 1:
            if tracking:
                tracking.append((i, j))
            puzzle[i][j] = choices.pop()
            return solve(puzzle, relatives, tracking)
    return True


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
    h = [(x, i) for i in range(9)]  #  horizontals
    v = [(i, y) for i in range(9)]  #  verticals
    x -= x%3
    y -= y%3
    d = [(x+i, y+j) for i, j in product(range(3), repeat=2)]  #  diagonals
    return set(h + v + d)


def cells():
    for i, j in product(range(9), repeat=2):
        yield (i, j)

def copy(puzzle):
    out = generate_empty_dic()
    for i, j in cells():
        out[i][j] = puzzle[i][j]
    return out


if __name__ == "__main__":
    hard = [[0, 0, 6, 1, 0, 0, 0, 0, 8], 
            [0, 8, 0, 0, 9, 0, 0, 3, 0], 
            [2, 0, 0, 0, 0, 5, 4, 0, 0], 
            [4, 0, 0, 0, 0, 1, 8, 0, 0], 
            [0, 3, 0, 0, 7, 0, 0, 4, 0], 
            [0, 0, 7, 9, 0, 0, 0, 0, 3], 
            [0, 0, 8, 4, 0, 0, 0, 0, 6], 
            [0, 2, 0, 0, 5, 0, 0, 8, 0], 
            [1, 0, 0, 0, 0, 2, 5, 0, 0]]

    easy = [[0, 0, 0, 4, 0, 8, 1, 5, 0], 
            [1, 0, 5, 6, 0, 3, 2, 0, 0], 
            [0, 0, 0, 9, 1, 5, 7, 0, 0], 
            [2, 5, 6, 0, 0, 1, 9, 0, 4], 
            [0, 9, 0, 0, 0, 0, 0, 2, 0], 
            [4, 0, 3, 8, 0, 0, 6, 1, 5], 
            [0, 0, 8, 3, 4, 9, 0, 0, 0], 
            [0, 0, 9, 2, 0, 6, 4, 0, 3], 
            [0, 6, 4, 1, 0, 7, 0, 0, 0]]
    
    issue = [[0, 0, 6, 3, 0, 0, 0, 0, 2],
             [0, 3, 0, 0, 4, 0, 0, 6, 0],
             [7, 0, 0, 0, 0, 1, 9, 0, 0],
             [2, 0, 0, 0, 0, 8, 7, 0, 0],
             [0, 1, 0, 0, 5, 0, 0, 4, 0],
             [0, 0, 9, 1, 0, 0, 0, 0, 5],
             [0, 0, 7, 4, 0, 0, 0, 0, 8],
             [0, 9, 0, 0, 1, 0, 0, 2, 0],
             [3, 0, 0, 0, 0, 5, 6, 0, 0]]


    issue2 = [[6, 0, 0, 0, 0, 0, 0, 0, 2],
              [0, 0, 3, 6, 0, 1, 7, 0, 0],
              [0, 7, 0, 0, 4, 0, 0, 1, 0],
              [0, 5, 0, 9, 0, 4, 0, 3, 0],
              [0, 0, 9, 0, 0, 0, 1, 0, 0],
              [0, 6, 0, 7, 0, 8, 0, 2, 0],
              [0, 3, 0, 0, 6, 0, 0, 5, 0],
              [0, 0, 5, 3, 0, 9, 4, 0, 0],
              [7, 0, 0, 0, 0, 0, 0, 0, 3]]

    issue3 = [[0, 9, 0, 0, 7, 1, 0, 0, 4],
              [2, 0, 0, 0, 0, 0, 0, 7, 0],
              [0, 0, 3, 0, 0, 0, 2, 0, 0],
              [0, 0, 0, 9, 0, 0, 0, 3, 5],
              [0, 0, 0, 0, 1, 0, 0, 8, 0],
              [7, 0, 0, 0, 0, 8, 4, 0, 0],
              [0, 0, 9, 0, 0, 6, 0, 0, 0],
              [0, 1, 7, 8, 0, 0, 0, 0, 0],
              [6, 0, 0, 0, 2, 0, 7, 0, 0]]

    issue4 = [[0, 0, 2, 0, 0, 1, 0, 0, 0],
              [3, 0, 0, 6, 8, 0, 7, 0, 0],
              [0, 0, 0, 5, 0, 0, 6, 0, 0],
              [0, 0, 7, 0, 0, 4, 0, 0, 0],
              [0, 0, 4, 0, 1, 7, 0, 0, 9],
              [0, 0, 0, 9, 0, 0, 8, 0, 0],
              [7, 0, 5, 0, 2, 0, 0, 3, 0],
              [0, 1, 0, 0, 0, 0, 0, 5, 0],
              [0, 8, 0, 0, 4, 0, 9, 0, 1]]

    issue5 = [[0, 0, 0, 0, 9, 0, 5, 0, 3],
              [0, 4, 5, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 6, 4, 0, 0],
              [0, 0, 9, 0, 0, 2, 0, 0, 0],
              [0, 1, 0, 9, 8, 4, 0, 6, 0],
              [0, 0, 0, 5, 0, 0, 2, 0, 0],
              [0, 0, 1, 8, 0, 0, 0, 0, 0],
              [2, 0, 0, 0, 0, 0, 1, 8, 0],
              [8, 0, 3, 0, 7, 0, 0, 0, 0]]

    solved = sudoku_solver(issue5)
    print_puzzle(solved)
