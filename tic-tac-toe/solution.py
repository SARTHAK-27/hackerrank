#!/bin/python
import random

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# Moves
_ = 0
X = 1
O = 2

# Move mapping
MOVES = {
    'X': X,
    'O': O,
    '_': _
}
STRINGS = {
    X: 'X',
    O: 'O',
    _: '_'
}
# Sample board grid
EMPTY = [
    [_,_,_],
    [_,_,_],
    [_,_,_],
]
# Player map
PLAYERS = {
    'X': X,
    'O': O
}
# Opponent map
OPPONENTS = {
    X: O,
    O: X
}
# Board corner coordinates
CORNERS = [
    (0,0),
    (0,2),
    (2,0),
    (2,2)
]
# Coordinate translations
COUNTER = {
    (0,0): (2,0),
    (0,1): (1,0),
    (0,2): (0,0),
    (1,0): (2,1),
    (1,1): (1,1),
    (1,2): (0,1),
    (2,0): (2,2),
    (2,1): (1,2),
    (2,2): (0,2),
}
CLOCKWISE = {}
for k, v in COUNTER.items():
    CLOCKWISE[v] = k

S = 8 # Blockable position
N = 6 # Forkable position

FORK_PATTERNS = [[
    [N,S,N],
    [S,S,0],
    [N,0,0]
],[
    [N,0,0],
    [N,N,S],
    [S,0,S]
],[
    [0,0,N],
    [S,N,N],
    [S,0,S]
],[
    [S,0,N],
    [N,S,0],
    [N,0,0]
],[
    [N,0,S],
    [0,S,N],
    [0,0,N]
],[
    [0,0,N],
    [0,S,0],
    [N,N,S]
],[
    [N,0,0],
    [0,S,0],
    [S,N,N]
],[
    [N,S,N],
    [0,N,0],
    [S,0,S]
]]

P = _ # Playable spot indicator

# Direct game plays to account for edge cases, generally these
# are all plays that pre-block any potential fork that is not 
# detected in the fork pattern routines.
DIRECT_PLAYS = {
    O: [[ 
        (2,1), [
            [X,_,_],
            [_,O,_],
            [_,P,X]
        ]
    ], [ 
        (0,1), [
            [X,P,_],
            [_,O,X],
            [_,_,_]
        ]
    ], [ 
        (1,2), [
            [_,X,_],
            [_,O,P],
            [_,_,X]
        ]
    ], [ 
        (2,0), [
            [O,_,_],
            [_,X,_],
            [P,_,X],
        ]
    ]],
    X: [] # Should already be playing best move
}


# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------

# Random move helper
def _ran():
    return random.randint(0, 2)

# Convert string rows into list
def _parseBoard(board):
    grid = []
    for r in board:
        data = []
        for k in r:
            data.append(MOVES[k])
        grid.append(data)
    return grid

def _stringBoard(board):
    grid = []
    for r in board:
        data = ''
        for k in r:
            data += STRINGS[k]
        grid.append(data)
    return grid


# Rotate board counter clockwise
def _rotate(b):
    return [
        [row[2] for row in b],
        [row[1] for row in b],
        [row[0] for row in b],
    ]

def _get_diagonals(b):
    return [
        [ b[0][0], b[1][1], b[2][2] ],
        [ b[0][2], b[1][1], b[2][0] ],
    ]


def analize_pattern(pattern, p, b):
    op = OPPONENTS[p]
    matches = 0
    needed = 0
    blocks = 0
    opened = 0
    t = 0
    for row in pattern:
        l = 0
        for k in row:
            if k == N: needed += 1 # Required for fork
            if k == S: opened += 1 # Blockable position

            val = b[t][l] # Board value
            if val == p: matches += 1 # Player has spot
            if val == op: blocks += 1 # Opponent has spot
            l += 1
        t += 1

    if needed - matches != 1: return False # Cant create fork
    if opened - blocks < 2: return False # Not possible, blocked

    for row in pattern:
        t = pattern.index(row)
        for k in row:
            if k != N: continue
            l = row.index(k)
            if b[t][l] == _: return (t, l)

    return False # No move


# ------------------------------------------------------------------------------
# Game engine
# ------------------------------------------------------------------------------

# 0. Check for best first move
def first_move(p, b):
    if p == X and b == EMPTY:
        random.shuffle(CORNERS)
        return CORNERS[0]
    return False

# 1. If the player has two in a row, he or she can place a third to get three in a row
def win(p, b):
    # Check horizontals
    for row in b:
        if row.count(_) != 1: continue # Must have one open spot
        if row.count(p) != 2: continue # Player needs two out of three
        return (b.index(row), row.index(_)) # Three in a row

    # Check verticals
    rotated = _rotate(b)
    for row in rotated:
        if row.count(_) != 1: continue # Must have one open spot
        if row.count(p) != 2: continue # Player needs two out of three
        return CLOCKWISE[(rotated.index(row), row.index(_))] # Three in a row

    # Check diagonals
    diagonals = _get_diagonals(b)
    for row in diagonals:
        if row.count(_) != 1: continue # Must have one open spot
        if row.count(p) != 2: continue # Player needs two out of three
        pos = row.index(_)
        if diagonals.index(row) == 1: return CLOCKWISE[(pos, pos)]
        return (pos, pos)

    return False # No moves found


# 2. If the [opponent] has two in a row, the player must play the third himself or herself to block them
def block(p, b):
    return win(OPPONENTS[p], b)

# 2b. Check for direct plays, handles edge cases
def check_direct_plays(p, b):
    for move, board in DIRECT_PLAYS[p]:
        for i in range(0, 4):
            move = COUNTER[move]
            board = _rotate(board)
            if board == b: return move
    return False

# 3. Creation of an opportunity where the player has two threats to win (two non-blocked lines of 2)
def fork(p, b):
    op = OPPONENTS[p]
    random.shuffle(FORK_PATTERNS)
    for pattern in FORK_PATTERNS:
        for i in range(0, 4):
            pattern = _rotate(pattern)
            matches = 0
            needed = 0
            blocks = 0
            opened = 0
            t = 0
            for row in pattern:
                l = 0
                for k in row:
                    if k == N: needed += 1 # Required for fork
                    if k == S: opened += 1 # Blockable position

                    val = b[t][l] # Board value
                    if val == p: matches += 1 # Player has spot
                    if val == op: blocks += 1 # Opponent has spot
                    l += 1
                t += 1

            if needed - matches != 1: return False # Cant create fork
            if opened - blocks < 2: return False # Not possible, blocked

            for row in pattern:
                t = pattern.index(row)
                for k in row:
                    if k != N: continue
                    l = row.index(k)
                    if b[t][l] == _: return (t, l)

    return False # No moves found


# 4. Block existing or potential fork

# 4a. If there is a configuration where the opponent can fork, 
# the player should block that fork
def block_fork(p, b):
    return fork(OPPONENTS[p], b)


# 4b. The player should create two in a row to force the opponent into 
# defending, as long as it doesn't result in them creating a fork
def force_defend(p, b):
    # Check horizontals
    for row in b:
        if row.count(_) != 2: continue
        if row.count(p) != 1: continue
        l = row.index(p) + 1
        if l > 2: l = 1
        return (b.index(row), l)

    # Check verticals
    rotated = _rotate(b)
    for row in rotated:
        if row.count(_) != 2: continue
        if row.count(p) != 1: continue
        l = row.index(p) + 1
        if l > 2: l = 1
        return CLOCKWISE[(rotated.index(row), l)]

    # Check diagonals
    diagonals = _get_diagonals(b)
    for row in diagonals:
        if row.count(_) != 2: continue
        if row.count(p) != 1: continue
        pos = row.index(p) + 1
        if pos > 2: pos = 1
        if diagonals.index(row) == 1: return CLOCKWISE[(pos, pos)]
        return (pos, pos)

    return False # No moves found


# 5. A player marks the center
def center(p, b):
    if b[1][1] == _: # Check for empty space
        return (1,1)
    return False # No moves found


# 6. If the opponent is in the corner, the player plays the opposite corner
def opposite_corner(p, b):
    op = OPPONENTS[p]
    if b[0][0] == op and b[2][2] == _: return (2,2)
    if b[0][2] == op and b[2][0] == _: return (2,0)
    if b[2][2] == op and b[0][0] == _: return (0,0)
    if b[2][0] == op and b[0][2] == _: return (0,2)
    return False


# 7. The player plays in a corner square
def empty_corner(p, b):
    if b[0][0] == _: return (0,0)
    if b[0][2] == _: return (0,2)
    if b[2][2] == _: return (2,2)
    if b[2][0] == _: return (2,0)
    return False # No moves found


# 8. The player plays in a middle square on any of the 4 sides
def empty_side(p, b):
    # Check horizontals
    for row in b:
        if row.count(_) != 3: continue # Row must be empty
        return (b.index(row), 1)

    # Check verticals
    rotated = _rotate(b)
    for row in rotated:
        if row.count(_) != 3: continue # Row must be empty
        return CLOCKWISE[(rotated.index(row), 1)]
    
    return False


# 9. Find any empty space on the board and play
def random_play(p, b):
    t = _ran()
    l = _ran()
    row = b[t]
    if row[l] == _: return (t, l) # First empty space
    return random_play(p, b) # Recurse until move found

# ------------------------------------------------------------------------------
# Game input
# ------------------------------------------------------------------------------

# Complete the function below to print 2 integers separated by a single space which will be your next move 
def nextMove(player, board):
    # Normalize input
    p = PLAYERS[player]
    b = _parseBoard(board=board)
    # Find best possible move
    move = (
        first_move(p, b)
        or win(p, b)
        or block(p, b)
        or check_direct_plays(p, b)
        or fork(p, b)
        or block_fork(p, b)
        or center(p, b)
        or opposite_corner(p, b)
        or empty_corner(p, b)
        or empty_side(p, b)
        or random_play(p, b)
    )
    print '%d %d' % move


# ------------------------------------------------------------------------------
# Test
# ------------------------------------------------------------------------------

player = raw_input()
board = []
for i in xrange(0, 3):
    board.append(raw_input())

nextMove(player, board)
