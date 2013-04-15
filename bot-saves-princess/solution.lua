-- --------------------------------------------------
-- https://www.hackerrank.com/challenges/saveprincess
-- --------------------------------------------------
-- Sample input
-- --------------------------------------------------
-- 3
-- ---
-- -m-
-- p--
-- --------------------------------------------------

-- Board information
local size = tonumber(io.read())
local i = 0
local board = {}

-- Position information
local mx = 0
local my = 0
local px = 0
local py = 0

-- Get board from input
while i < size do
  board[i + 1] = io.read()
  i = i + 1
end

-- Find positions
for y, line in ipairs(board) do
  -- Find player position
  local x = string.find(line, 'm')
  if x then
    my = y
    mx = x
  end
  -- Find princess position
  local x = string.find(line, 'p')
  if x then
    py = y
    px = x
  end
end

-- Check left and right
if mx > px then
  while mx > px do
    print('LEFT')
    mx = mx - 1
  end
elseif mx < px then
  while mx < px do
    print('RIGHT')
    mx = mx + 1
  end
end

-- Check up and down
if my > py then
  while my > py do
    print('UP')
    my = my - 1
  end
elseif my < py then
  while my < py do
    print('DOWN')
    my = my + 1
  end
end
