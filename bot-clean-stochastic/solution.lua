
-- ----------------------------------------------
-- https://www.hackerrank.com/challenges/botclean
-- ----------------------------------------------
-- Sample input
-- ----------------------------------------------
-- 0 0
-- b---d
-- -----
-- -----
-- -----
-- -----
-- ----------------------------------------------

-- Board information
local xy = io.read()
local i = 0
local board = {}
local size = 5

-- Position information
local by = tonumber(xy:sub(1, 1)) + 1
local bx = tonumber(xy:sub(-1)) + 1
local dx = 0
local dy = 0
local dirty = {}

-- Get board from input
while i < size do
  board[i + 1] = io.read()
  i = i + 1
end

-- Find positions
for y, line in ipairs(board) do
  -- Find dirty position(s)
  local x = string.find(line, 'd')
  if x then
    dy = y
    dx = x
    break
  end
end

-- Output
if bx == dx and by == dy then
  print('CLEAN')
elseif bx < dx then
  print('RIGHT')
elseif by < dy then
  print('DOWN')
elseif bx > dx then
  print('LEFT')
elseif by > dy then
  print('UP')
end