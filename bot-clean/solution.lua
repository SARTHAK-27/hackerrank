
-- ----------------------------------------------
-- https://www.hackerrank.com/challenges/botclean
-- ----------------------------------------------
-- Sample input
-- ----------------------------------------------
-- 0 0
-- b---d
-- -d--d
-- --dd-
-- --d--
-- ----d
-- ----------------------------------------------

-- Board information
local xy = io.read()
local i = 0
local board = {}
local size = 5

-- Position information
local by = tonumber(xy:sub(1, 1)) + 1
local bx = tonumber(xy:sub(-1)) + 1
local dirty = {}

-- Get board from input
while i < size do
  board[i + 1] = io.read()
  i = i + 1
end

-- Find positions
for y, line in ipairs(board) do
  -- Find dirty positions

  i = 1
  while i <= size do
    local x = line:sub(i, i)
    if x == 'd' then
      dirty[#dirty + 1] = {i, y}
    end
    i = i + 1
  end
end

print(bx, by)
for _, line in ipairs(dirty) do
  print(unpack(line))
end

-- 1 1

-- 2 2 - 2
-- 5 1 - 4
-- 3 3 - 4
-- 5 2 - 5
-- 4 3 - 5
-- 3 4 - 5
-- 5 5 - 8


-- 2 2 
-- 5 1 
-- 3 3 
-- 5 2 
-- 4 3 
-- 3 4 
-- 5 5 