import time, random

def solve_all(grids, name = '', showif= 0.0):
    def time_solve(grid):
        start = time.perf_counter()
        values = solve(grid)
        t = time.perf_counter()-start
        if showif is not None and t > showif:
            display(grid_values(grid))
            if values:
                display(values)
            print('(%.2f seconds)\n' % t)
        return (t, solved(values))
    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        print("Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)."%(sum(results), N, name, sum(times)/N, N/sum(times), max(times)))

def solved(values):
    def unitsolved(unit):
        return set(values[s] for s in unit) == set(digits)
    return values is not False and all(unitsolved(unit) for unit in unitlist)

# def from_file(filename, sep='\n'):
#     return file(filename).read().strip().split(sep)

# def random_puzzle(N=17):
#     values = dict((s, digits) for s in squares)
#     for s in shuffled(squares):
#         if not assign(values, s, random.choice(values[s])):
#             break
#         ds = [values[s] for s in squares if len(values[s]) == 1]
#         if len(ds) >= N and len(set(ds)) >= 8:
#             return ''.join(values[s] if len(values[s]) == 1 else '.' for s in squares)
#         return random_puzzle(N)

# def shuffled(seq):
#     seq = list(seq)
#     random.shuffle(seq)
#     return seq
def test():
    assert len(squares) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 20 for s in squares)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'], ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == {'C5', 'D2', 'C6', 'A3', 'B2', 'A2', 'C7', 'G2', 'F2', 'B3', 'C1', 'C4', 'I2', 'B1', 'H2', 'A1', 'E2', 'C3', 'C8', 'C9'}
    print("All tests pass")


def cross(A, B):
    return [a+b for a in A for b in B]

def grid_values(grid):
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))

def parse_grid(grid):
    values = dict((s, digits) for s in squares)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False
    return values

def assign(values, s, d):
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

def solve(grid):
    return search(parse_grid(grid))


def search(values):
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in squares):
        return values
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d)) for d in values[s])

def some(seq):
    for e in seq:
        if e: return e
    return False

def eliminate(values, s, d):
    if d not in values[s]:
        return values
    values[s] = values[s].replace(d,'')
    if len(values[s]) == 0:
        return False
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False
        elif len(dplaces) == 1:
            if not assign(values, dplaces[0], d):
                return False
    return values

def display(grid):
    for r in rows:
        s = ""
        for d in digits:
            if len(s) == 6 or len(s) == 13:
                s = s + "|"
            s = s + grid[r+d] + " "
        print(s)
        if r == "C" or r == "F":
            print("------+------+------")
    
digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)
#print(squares)
unitlist = [cross(rows, c) for c in cols]+[cross(r, cols) for r in rows]+[cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#print(unitlist)
units = dict((s, [u for u in unitlist if s in u]) for s in squares)
#print(units)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in squares)
#print(peers)
#test()
grid = "85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4."
print(len(grid))
#display(solve(grid))
solve_all([grid])
