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

Section:NewButton("MM2 Auto Farmer", "Loads a farmer lua", function(ff)
loadstring(game:HttpGet("https://raw.githubusercontent.com/Aura-56/MurderMystery2/refs/heads/main/Autofarm.lua"))()
end)

