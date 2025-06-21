# Получаем путь к текущей директории скрипта (cwd)
$cwd = Split-Path -Parent $MyInvocation.MyCommand.Path

# Определяем пути
$base = Join-Path $cwd "data\Source"

# Массив подкаталогов и количество дней назад
$folders = @{
    "A_recent" = 1
    "B_mid"    = 5
    "C_old"    = 15
}

# Создание структуры
foreach ($name in $folders.Keys) {
    $sub = Join-Path $base $name
    New-Item -ItemType Directory -Path $sub -Force | Out-Null

    $file = Join-Path $sub "test.txt"
    Set-Content -Path $file -Value "Test for $name"

    $daysAgo = $folders[$name]
    $date = (Get-Date).AddDays(-$daysAgo)

    # Устанавливаем дату создания, изменения и доступа
    (Get-Item $file).CreationTime = $date
    (Get-Item $file).LastWriteTime = $date
    (Get-Item $file).LastAccessTime = $date
}

Write-Host "✅ Тестовая структура создана в $base" -ForegroundColor Green
