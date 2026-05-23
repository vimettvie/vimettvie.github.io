local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")
local player = Players.LocalPlayer

_G.AutoFarm = false
_G.CoinsCollected = 0

-- Функція для отримання контейнера з перевіркою
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
            local container = getCoinContainer()
            
            -- Якщо карти немає — стоїмо і чекаємо, нікуди не ліземо
            if not container or not container.Parent then
                print("Чекаємо на завантаження нової карти...")
                task.wait(10) -- Пауза перед новим пошуком
                continue 
            end
            
            -- Якщо контейнер є, збираємо
            local coins = container:GetChildren()
            for _, coin in pairs(coins) do
                -- ПЕРЕВІРКА: якщо карта змінила під час циклу
                if not container or not container.Parent then break end 
                if not _G.AutoFarm then break end
                
                if coin:IsA("BasePart") and coin.Parent ~= nil then
                    local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart")
                    if root then
                        local dist = (root.Position - coin.Position).Magnitude
                        local tween = TweenService:Create(root, TweenInfo.new(dist / 40, Enum.EasingStyle.Linear), {CFrame = coin.CFrame})
                        tween:Play()
                        tween.Completed:Wait()
                        
                        _G.CoinsCollected += 1
                        task.wait(0.3)
                    end
                end
                
                -- Ліміт 40 монет
                if _G.CoinsCollected >= 40 then
                    _G.CoinsCollected = 0
                    if player.Character then player.Character:BreakJoints() end
                    task.wait(10) -- Після ресету чекаємо 10 сек
                    break 
                end
            end
        end
    end
end)
