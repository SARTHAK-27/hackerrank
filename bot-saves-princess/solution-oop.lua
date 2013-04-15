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

local Bot = {}

-- Bot constructor
function Bot:new(o)
  o = o or {}
  setmetatable(o, self)
  self.__index = self
  self.board = {}
  self.b_char = 'm' -- Player character
  self.p_char = 'p' -- Princess character
  self.left = 'LEFT'
  self.right = 'RIGHT'
  self.up = 'UP'
  self.down = 'DOWN'
  return o
end

-- Get game input information
function Bot:input()
  self.size = tonumber(io.read())
  local i = 0
  while i < self.size do
    self.board[i + 1] = io.read()
    i = i + 1
  end
  self.player = self:find(self.b_char)
  self.princess = self:find(self.p_char)
  return self
end

-- Get x, y position of given character in board
function Bot:find(char)
  for y, line in ipairs(self.board) do
    local x = string.find(line, char)
    if x then
      return {x, y}
    end
  end
end

-- Find left and right outputs
function Bot:left_right()
  local x = self.player[1]
  local t = self.princess[1]
  if x > t then
    while x > t do
      print(self.left)
      x = x - 1
    end
  elseif x < t then
    while x < t do
      print(self.right)
      x = x + 1
    end
  end
  return self
end

-- Find up and down outputs
function Bot:up_down()
  local y = self.player[2]
  local t = self.princess[2]
  if y > t then
    while y > t do
      print(self.up)
      y = y - 1
    end
  elseif y < t then
    while y < t do
      print(self.down)
      y = y + 1
    end
  end
  return self
end

-- Determine output information
function Bot:output()
  self:left_right()
  self:up_down()
  return self
end

local bot = Bot:new():input():output()
