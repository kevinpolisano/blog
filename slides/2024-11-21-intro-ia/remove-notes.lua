function Div(el)
  -- Supprime les Div avec la classe "notes"
  if el.classes:includes("notes") then
    print("Suppression d'un bloc notes (Div)")
    return {} -- Supprime complètement le Div
  end
  return el
end


