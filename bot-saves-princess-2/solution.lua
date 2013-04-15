-- ---------------------------------------------------
-- https://www.hackerrank.com/challenges/saveprincess2
-- ---------------------------------------------------
-- Sample input
-- ---------------------------------------------------
-- 5
-- 2 2
-- -----
-- -----
-- p-m--
-- -----
-- -----
-- ---------------------------------------------------

-- Board information
local size = tonumber(io.read())
local i = 0
local board = {}
local xy = io.read()

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

-- Output
if mx > px then
  print('LEFT')
elseif mx < px then
  print('RIGHT')
elseif my > py then
  print('UP')
elseif my < py then
  print('DOWN')
end
