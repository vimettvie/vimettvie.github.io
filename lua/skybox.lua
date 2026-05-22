local Lighting = game:GetService("Lighting")
for _, v in pairs(Lighting:GetChildren()) do
    if v:IsA("Sky") then v:Destroy() end
end
local MySky = Instance.new("Sky")
MySky.Parent = Lighting
local Lib = loadstring(game:HttpGet("https://raw.githubusercontent.com/xHeptc/Kavo-UI-Library/main/source.lua"))()
local Win = Lib.CreateLib("Sky Changer", "Midnight")
local Tab = Win:NewTab("Sky")
local Sec = Tab:NewSection("Presets")

local function SetSky(id, col)
    MySky.SkyboxBk = id
    MySky.SkyboxDn = id
    MySky.SkyboxFt = id
    MySky.SkyboxLf = id
    MySky.SkyboxRt = id
    MySky.SkyboxUp = id
    Lighting.Ambient = col
    Lighting.OutdoorAmbient = col
end

Sec:NewButton("Neon", "Set Neon", function()
    SetSky("rbxassetid://600831433", Color3.fromRGB(0,0,50))
end)

Sec:NewButton("Sunset", "Set Sunset", function()
    SetSky("rbxassetid://600831433", Color3.fromRGB(255,100,50))
end)

Sec:NewButton("Space", "Set Space", function()
    SetSky("rbxassetid://600831433", Color3.fromRGB(20,20,20))
end)

local CSec = Tab:NewSection("Color Picker")
CSec:NewColorPicker("Ambient", "Custom Color", Color3.fromRGB(255,255,255), function(c)
    Lighting.Ambient = c
    Lighting.OutdoorAmbient = c
end)
