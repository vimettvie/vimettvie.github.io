local Library = loadstring(game:HttpGet("https://raw.githubusercontent.com/xHeptc/Kavo-UI-Library/main/source.lua"))()
local Window = Library.CreateLib("Basic Loader", "BloodTheme")
local Tab = Window:NewTab("main")
local Section = Tab:NewSection("Walk")
local spd = 16
local jmp = 50
local human = game.Players.LocalPlayer.Character.Humanoid
local player = game.Players.LocalPlayer

Section:NewSlider("Speed", "idk", 800, 16, function(s)
    spd = s
end)

local Section = Tab:NewSection("Jump")
Section:NewSlider("jump", "idk", 800, 50, function(j)
    jmp = j
end)

task.spawn(function()
	while true do
			local char = player.Character
			if char and char.FindFirstChild("Humanoid") then
				local human = char.Humanoid
				human.WalkSpeed = spd
				human.JumpPower = jmp
			end
		task.wait()
	end
end)

local Section = Tab:NewSection("Scripts")

Section:NewButton("Sky Changer", "Loads a sky changer lua", function(hi)
loadstring(game:HttpGet("https://www.inhook.xyz/lua/skybox.lua"))()
end)

Section:NewButton("MM2 Auto Farmer", "Loads a farmer lua", function(gkg)
loadstring(game:HttpGet("https://raw.githubusercontent.com/Aura-56/MurderMystery2/refs/heads/main/Autofarm.lua"))()
end)

Section:NewButton("Optimaz", "zssvvk", function(bf)
local RunService = game:GetService("RunService")
local Lighting = game:GetService("Lighting")
local Workspace = game:GetService("Workspace")
local function optimizeGame()
    Lighting.GlobalShadows = false
    Lighting.Brightness = 2
    Lighting.OutdoorAmbient = Color3.fromRGB(150, 150, 150)
    Lighting.FogEnd = 100000
    for _, obj in pairs(Workspace:GetDescendants()) do
        if obj:IsA("Decal") or obj:IsA("Texture") or 
           obj:IsA("Sparkles") or obj:IsA("Fire") or 
           obj:IsA("Smoke") or obj:IsA("PostEffect") then
            obj:Destroy()
        elseif obj:IsA("Part") or obj:IsA("MeshPart") or obj:IsA("UnionOperation") then
            obj.Material = Enum.Material.Plastic
            obj.Reflectance = 0
        end
    end
    for _, effect in pairs(Lighting:GetChildren()) do
        if effect:IsA("Atmosphere") or effect:IsA("BloomEffect") or 
           effect:IsA("SunRaysEffect") or effect:IsA("BlurEffect") then
            effect:Destroy()
        end
    end
    
    print("Optimization: Done, bro! 🧊")
end
optimizeGame()
Workspace.DescendantAdded:Connect(function(obj)
    if obj:IsA("Decal") or obj:IsA("Texture") or obj:IsA("Sparkles") then
        obj:Destroy()
    end
end)
end)
