-- Written by ChatGPT
-- This Lua filter will replace .md links with .html
function Link(el)
  -- Check if the link destination ends with .md
  if el.target:match("%.md$") then
    -- Replace .md with .html
    el.target = el.target:sub(1, -4) .. ".html"
  end
  return el
end
