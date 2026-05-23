local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")
local player = Players.LocalPlayer
local playerGui = player:WaitForChild("PlayerGui")

_G.AutoFarm = false
_G.CoinsCollected = 0

-- GUI: Кнопка керування
local screenGui = Instance.new("ScreenGui", playerGui)
local button = Instance.new("TextButton", screenGui)
button.Size = UDim2.new(0, 150, 0, 50)
button.Position = UDim2.new(0.5, -75, 0.9, -50)
button.Text = "Start AutoFarm"
button.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
button.TextColor3 = Color3.new(1, 1, 1)

button.MouseButton1Click:Connect(function()
    _G.AutoFarm = not _G.AutoFarm
    button.Text = _G.AutoFarm and "Stop AutoFarm" or "Start AutoFarm"
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
    while task.wait(0.5) do
        if _G.AutoFarm then
            local char = player.Character
            local root = char and char:FindFirstChild("HumanoidRootPart")
            local humanoid = char and char:FindFirstChild("Humanoid")
            local container = getCoinContainer()

            -- Якщо ти вмер або карти ще нема — просто нічого не робимо
            if not root or (humanoid and humanoid.Health <= 0) or not container or not container.Parent then
                continue 
            end

            -- Збір монет
            local coins = container:GetChildren()
            for _, coin in pairs(coins) do
                -- Перевірка на випадок смерті або вимкнення під час руху
                if not _G.AutoFarm or not player.Character or player.Character.Humanoid.Health <= 0 then break end
                
                if coin:IsA("BasePart") and coin.Parent ~= nil then
                    -- Розрахунок плавності руху (швидкість 40)
                    local dist = (root.Position - coin.Position).Magnitude
                    local tween = TweenService:Create(root, TweenInfo.new(dist / 40, Enum.EasingStyle.Linear), {CFrame = coin.CFrame})
                    tween:Play()
                    tween.Completed:Wait()
                    
                    _G.CoinsCollected += 1
                    task.wait(0.3)
                end
                
                -- Ресет після 40 монет
                if _G.CoinsCollected >= 40 then
                    _G.CoinsCollected = 0
                    if player.Character then player.Character:BreakJoints() end
                    
                    -- Чекаємо 10 секунд після ресету (поки карта зміниться)
                    task.wait(10) 
                    break 
                end
            end
        end
    end
end)
