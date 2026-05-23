local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")
local player = Players.LocalPlayer
local playerGui = player:WaitForChild("PlayerGui")

_G.AutoFarm = false
_G.CoinsCollected = 0

-- GUI: Тепер має бути видно на 100%
local screenGui = Instance.new("ScreenGui", playerGui)
screenGui.Name = "FarmGUI"
screenGui.ResetOnSpawn = false

local button = Instance.new("TextButton", screenGui)
button.Size = UDim2.new(0, 200, 0, 60)
button.Position = UDim2.new(0.5, -100, 0.8, 0)
button.Text = "Start AutoFarm"
button.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
button.TextColor3 = Color3.new(1, 1, 1)

button.MouseButton1Click:Connect(function()
    _G.AutoFarm = not _G.AutoFarm
    button.Text = _G.AutoFarm and "Stop" or "Start"
    button.BackgroundColor3 = _G.AutoFarm and Color3.fromRGB(0, 150, 0) or Color3.fromRGB(50, 50, 50)
end)

local function getCoinContainer()
    for _, obj in pairs(workspace:GetChildren()) do
        local c = obj:FindFirstChild("CoinContainer")
        if c then return c end
    end
    return nil
end

task.spawn(function()
    while task.wait(1) do
        if _G.AutoFarm then
            local container = getCoinContainer()
            if not container or not container.Parent then
                continue 
            end

            -- Чекаємо 10 секунд перед початком фарму нової карти
            task.wait(10)

            local coins = container:GetChildren()
            for _, coin in pairs(coins) do
                if not _G.AutoFarm or player.Character.Humanoid.Health <= 0 then break end
                
                if coin:IsA("BasePart") then
                    local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart")
                    if root then
                        -- Летимо до монети
                        local dist = (root.Position - coin.Position).Magnitude
                        local tween = TweenService:Create(root, TweenInfo.new(dist / 40, Enum.EasingStyle.Linear), {CFrame = coin.CFrame})
                        tween:Play()
                        tween.Completed:Wait()
                        
                        -- Тепер стоїмо на місці 0.5 сек, щоб гра точно зарахувала збір
                        task.wait(0.5) 
                        
                        _G.CoinsCollected += 1
                    end
                end
                
                if _G.CoinsCollected >= 40 then
                    _G.CoinsCollected = 0
                    if player.Character then player.Character:BreakJoints() end
                    break 
                end
            end
        end
    end
end)
