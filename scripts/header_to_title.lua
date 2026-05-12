-- Source - https://stackoverflow.com/a/76048743
-- Posted by johndoe
-- Retrieved 2026-05-12, License - CC BY-SA 4.0

local title
function Header(el)
  if title then return end
  title = pandoc.utils.stringify(el)
end

function Meta(el)
  if not el.pagetitle then
    el.pagetitle = title
    return el
  end
end

