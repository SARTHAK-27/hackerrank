
from copy import copy
import random
from sys import argv
TEST = False
if 'test' in argv: TEST = True

_ = '_'
R = 'X'
B = 'O'
STRINGS = {
    '-': '_',
    'r': 'X',
    'b': 'O'
}
OPPONENTS = {
    R: B,
    B: R
}
BOARD_SIZE = 9

# Multipliers for moving clockwise
QUADS = [
    ( 1,-1), # Bottom right
    (-1,-1), # Bottom left
    (-1, 1), # Top left
    ( 1, 1), # Top right
]

# Helpers
# ======================================

def next(obj, el):
    return obj[(obj.index(el) + 1) % len(obj)]


def valid(*args):
    for y, x in args:
        if not 0 <= y < BOARD_SIZE or not 0 <= x < BOARD_SIZE:
            return False
    return True


def output(p=None, board=None, moves=[]):
    if moves and not valid(*moves): return
    if not board:
        board = create_board()
        for y, x in moves:
            board[y][x] = p
    data = [' '.join(x) for x in board]
    out = ' #\n# '.join(data)
    print ''
    print '#'.join(['' for x in range(0, BOARD_SIZE*2 + 4)])
    print '# ' + out + ' #'
    print '#'.join(['' for x in range(0, BOARD_SIZE*2 + 4)])


# Calculations
# ======================================

def sides(size, y, x, start=0):
    start = QUADS[start]
    length = size - 1
    moves = []
    for q in range(0, len(QUADS)):
        start = next(obj=QUADS, el=start)
        u, r = start
        for i in range(0, size):
            if i == length: u, r = next(obj=QUADS, el=start)
            dy, dx = u, r
            if size == 2:
                if sum(start) == 0:
                    if i == 0: dx = 0
                    else: dy = 0
                else:
                    if i == 0: dy = 0
                    else: dx = 0
            else:
                if i == 0 or i == length:
                    if u + r == 0: dx = 0
                    else: dy = 0
            y += dy
            x += dx
            moves.append((y, x))
    return moves


def corners(size, y, x):
    start = QUADS[0]
    length = size - 1
    moves = []
    for q in range(0, len(QUADS)):
        start = next(obj=QUADS, el=start)
        u, r = start
        for i in range(0, size):
            if i == length: u, r = next(obj=QUADS, el=start)
            dy, dx = u, r
            if size != 2 and  0 < i < length:
                if u + r == 0:
                    dx *= 2
                    dy = 0
                else:
                    dx = 0
                    dy *= 2
            y += dy
            x += dx
            moves.append((y, x))
    return moves


def who(board, pos):
    y, x = pos
    return board[y][x]


def create_board():
    rng = range(0, BOARD_SIZE)
    line = [copy(_) for x in rng]
    return [copy(line) for x in rng]


def intersect(*args):
    shortest = 10000
    data = []
    for lst in args:
        if len(lst) < shortest: shortest = lst
    for el in shortest:
        ok = True
        for lst in args:
            if el not in lst:
                ok = False
                break
        if ok and el not in data: data.append(el)
    return data


testing = {}

# Game logic
# ======================================

def square(board, y, x, p):
    o = OPPONENTS[p]
    coord = (y, x) # Top right
    safe = []
    score = 0
    total = 0
    for size in range(2, BOARD_SIZE + 1): # All square sizes
        length = size - 1
        dy = y + length
        dx = x - length
        s1 = sides(size=size, y=dy, x=x) # Bottom right
        c1 = corners(size=size, y=dy, x=dx) # Bottom left
        s2 = sides(size=size, y=y, x=dx, start=1) # Top left

        for i in range(0, len(s1)):
            neg = 1
            tmp = 0
            ax = coord # Open spot
            bx = s1[i]
            cx = c1[i]
            dx = s2[i]
            if not valid(ax, bx, cx, dx): continue # Check bounds

            total += 1

            a = who(board=board, pos=ax)
            b = who(board=board, pos=bx)
            c = who(board=board, pos=cx)
            d = who(board=board, pos=dx)

            if TEST:
                if a == b == c == d == p: # Lost the game
                    output(p='Z', board=None, moves=[ax, bx, cx, dx])
            
            if b == c == d == p: # Losing move
                testing[(y,x)] = -1
                return -1
            
            if b == o or c == o or d == o: # Opponent has a spot
                if b == o: tmp -= 1
                if c == o: tmp -= 1
                if d == o: tmp -= 1
            else:
                if b == p: tmp += 1
                if c == p: tmp += 1
                if d == p: tmp += 1

            score += tmp

    score += total
    # if len(testing.keys()) != 81:
    testing[(y,x)] = total
    return max(0, score) # -1 is reserved for losing moves


def matches(target, board):
    data = []
    y = 0
    for row in board:
        x = 0
        for spot in row:
            if spot == target: data.append((y, x))
            x += 1
        y += 1
    return data


def get_scores(target, board):
    global testing
    testing = {}
    bad = [] # Will lose the game
    scored = {}
    empty = matches(target=_, board=board)
    for y, x in empty: # Go through all open spaces
        score = square(board=board, y=y, x=x, p=target)
        # safes.append(safe)
        if not testing.get((y,x)):
            import pdb; pdb.set_trace()
        pos = (y, x)
        if score == -1:
            bad.append(pos)
            break
        if pos in bad: continue
        if not scored.get(score): scored[score] = []
        if pos not in scored[score]: scored[score].append(pos)

    # Remove bad elements
    for pos in bad:
        for score, moves in scored.items():
            if pos in moves: scored[score].remove(pos)
    # Remove empties
    for score, moves in scored.items():
        if not moves: del scored[score]
    return scored, bad

gof = {R: False, B: False}
gob = {R: False, B: False}

def unique(obj):
    tmp = []
    for x in obj:
        if x not in tmp: tmp.append(x)
    return tmp


def mirror(p, board):
    o = OPPONENTS[p]
    ops = matches(target=o, board=board)
    for y, x in ops:
        iy = abs(y - 8)
        ix = abs(x - 8)
        if board[iy][ix] == _:
            return (iy, ix)
    return None


def play(p, board):
    o = OPPONENTS[p]
    opn = matches(target=_, board=board) # All open spaces
    turn = 81 - len(opn)
    player_turn = (((turn + 1) + turn % 2) / 2) - 1
    p_scores, p_bad = get_scores(target=p, board=board)
    o_scores, o_bad = get_scores(target=o, board=board)
    p_total = [] # Find all possible moves for player
    for k, val in p_scores.items():
        p_total += val
    p_total = unique(p_total)

    o_total = [] # Find all possible moves for player
    for k, val in o_scores.items():
        o_total += val
    o_total = unique(o_total)

    both = intersect(o_total, p_total)
    p_min = min(p_scores.keys()) if p_scores else -1 # Lowest player score
    o_min = min(o_scores.keys()) if o_scores else -1 # Lowest opponent score
    good = []
    pos = mirror(p=p, board=board)
    if pos:
        y, x = pos
        score = square(board=board, y=y, x=x, p=p)
        if score != -1:
            if pos not in p_total:
                beau, bbad = get_scores(target=p, board=board)
                blah = []
                for k, val in beau.items():
                    blah += val
                print pos in blah
                import pdb; pdb.set_trace()
            good = [pos]


    if p == B:
        if board[4][4] == o:
            good = []

    if not good:
        if p_min == o_min and p_scores:
            good = intersect(p_scores[p_min], o_scores[o_min])


    if not good and p_scores: good = p_scores[p_min] # Use best player moves if none shared
    if not good: good = opn # Going to lose, make a valid play anyways
    
    if p == R and turn == 0:
        return (4, 4)

    # 1) p2 always wins against p1 random
    # 2) p1 always wins against p2 in same order
    first = good[0]
    last = good[len(good) - 1]
    return good[random.randint(0, len(good)-1)] # Random move from the list


def in_row(p, board, y=0):
    count = 0
    for x in range(0, 9):
        if who(board=board, pos=(y, x)) == p: count += 1
    return count


def in_a_row(p, board, direction=1):
    count = 0
    for y in range(0, 9):
        if direction != 1: y = 8 - y
        for x in range(0, 9):
            if direction != 1: x = 8 - x
            if who(board=board, pos=(y, x)) != p: break
            count += 1
    return count


# Test match
# ======================================

def lost(board, y, x, p):
    score = square(board=board, y=y, x=x, p=p)
    if score == -1: return True
    return False


def match():
    board = create_board()
    p1 = R
    p2 = B
    p = p2
    for i in range(0, 81):
        p = OPPONENTS[p]
        y, x = play(p=p, board=board)
        if not valid((y, x)): raise Exception('OOB - P:%s - (%d,%d)' % (p, y, x))
        board[y][x] = p
        if lost(board=board, y=y, x=x, p=p):
            print 'Player %s Won - %d' % (OPPONENTS[p], i+1)
            if OPPONENTS[p] == p1: print 'AMAZING!!'
            board[y][x] = 'Z'
            break
        output(board=board)
    output(board=board)


if TEST: 
    match()
else:
    # Input
    # ======================================

    p = STRINGS[raw_input()]
    board = []
    for i in xrange(0, 9):
        board.append([STRINGS[x] for x in raw_input()])

    # Output
    # ======================================

    print '%d %d' % play(p=p, board=board)
