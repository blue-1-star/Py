# Путь к файлу requirements_part1.txt
$requirementsFile = "requirements.txt"

# Проверяем, существует ли файл
if (-Not (Test-Path $requirementsFile)) {
    Write-Host "Файл $requirementsFile не найден!" -ForegroundColor Red
    exit
}

# Получаем список библиотек из файла
$requiredLibraries = Get-Content $requirementsFile

# Получаем список уже установленных библиотек
$installedLibraries = pip list --format=freeze | ForEach-Object { $_.Split('==')[0] }

# Устанавливаем только те библиотеки, которые ещё не установлены
foreach ($library in $requiredLibraries) {
    $libraryName = $library.Split('==')[0]

    if ($installedLibraries -contains $libraryName) {
        Write-Host "Библиотека $libraryName уже установлена." -ForegroundColor Green
    } else {
        Write-Host "Устанавливаю библиотеку: $library" -ForegroundColor Yellow
        pip install $library

        # Проверяем, успешно ли установлена библиотека
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Ошибка при установке библиотеки $library!" -ForegroundColor Red
            exit
        }
    }
}

Write-Host "Все библиотеки успешно установлены!" -ForegroundColor Green