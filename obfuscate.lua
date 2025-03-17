function Inlines (inlines)
    local result = {}
    local buffer = {}
    local in_obfuscate = false

    for _, el in ipairs(inlines) do
        --print("Element Type:", el.t)
        --print("Element Content:", el.text or "(no text)")
        if el.t == "RawInline" and el.format == "html" then
            if el.text:match("<obfuscate>") then
                in_obfuscate = true
                print("Opening <obfuscate> tag found")
                table.insert(buffer, (el.text:gsub("<obfuscate>", "")))
            elseif el.text:match("</obfuscate>") then
                in_obfuscate = false
                print("Closing </obfuscate> tag found")
                table.insert(buffer, (el.text:gsub("</obfuscate>", "")))
                local handle = io.popen('echo "' .. table.concat(buffer):gsub("\n"," ") .. '" | base64 -')
                local obfuscated_content = (handle:read("*a"):gsub("\n", ""))
                handle:close()
                table.insert(
                    result,
                    pandoc.RawInline(
                        "html",
                        '<script type="text/javascript">document.write(window.atob("' .. obfuscated_content .. '"));</script>'))
                buffer = {}
            elseif in_obfuscate then
                table.insert(buffer, el.text)
            else
                table.insert(result, el)
            end
        elseif in_obfuscate then
            table.insert(buffer, pandoc.utils.stringify(el))
        else
            table.insert(result, el)
        end
    end

    return result
end
--[[
function Inlines (inlines)
    local result = {}
    local buffer = {}
    local in_obfuscate = false

    for _, el in ipairs(inlines) do
        if el.t == "RawInline" and el.format == "html" then
            if el.text:match("<obfuscate>") then
                in_obfuscate = true
                table.insert(buffer, el.text:gsub("<obfuscate>", ""))
            elseif el.text:match("</obfuscate>") then
                in_obfuscate = false
                table.insert(buffer, el.text:gsub("</obfuscate>", ""))
                local obfuscated_content = table.concat(buffer)
                table.insert(result, pandoc.RawInline("html", '<script>document.write("' .. obfuscated_content .. '");</script>'))
                buffer = {}
            elseif in_obfuscate then
                table.insert(buffer, el.text)
            else
                table.insert(result, el)
            end
        elseif in_obfuscate then
            table.insert(buffer, pandoc.utils.stringify(el))
        else
            table.insert(result, el)
        end
    end

    return result
end
function Inlines (inlines)
    local text = pandoc.utils.stringify(inlines)
    local replaced = text:gsub(
        "<obfuscate>(.-)</obfuscate>",
        function(content)
            return '<script>document.write("' .. content .. '");</script>'
        end
    )
    return pandoc.RawInline("html", replaced)
end
function RawBlock(el)
    if el.format == "html" then
        print(el.text)
        local replaced = el.text:gsub(
            "<obfuscate>(.-)</obfuscate>",
            function(content)
                return '<script>document.write("' .. content .. '");</script>'
            end
        )
        return pandoc.RawBlock("html", replaced)
    end
end
function RawInline(el)
    if el.format == "html" then
        print(el.text)
        local replaced = el.text:gsub(
            "<obfuscate>(.-)</obfuscate>",
            function(content)
                return '<script>document.write("' .. content .. '");</script>'
            end
        )
        return pandoc.RawInline("html", replaced)
    end
end
--]]
