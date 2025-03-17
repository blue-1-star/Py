# Путь к файлу requirements_part1.txt
$requirementsFile = "requirements_part1.txt"

# Путь к лог-файлу
$logFile = "install_log.txt"

# Начало логгирования
Start-Transcript -Path $logFile -Append

# Проверяем, существует ли файл
if (-Not (Test-Path $requirementsFile)) {
    Write-Host "Файл $requirementsFile не найден!" -ForegroundColor Red
    exit
}

# Получаем список библиотек из файла
$requiredLibraries = Get-Content $requirementsFile

# Получаем список уже установленных библиотек
$installedLibraries = pip list --format=freeze | ForEach-Object { $_.Split('==')[0] }

# Счётчики для отчёта
$totalLibraries = $requiredLibraries.Count
$alreadyInstalled = 0
$installedInSession = 0
$failedLibraries = @()

# Устанавливаем только те библиотеки, которые ещё не установлены
foreach ($library in $requiredLibraries) {
    $libraryName = $library.Split('==')[0]

    if ($installedLibraries -contains $libraryName) {
        Write-Host "Библиотека $libraryName уже установлена." -ForegroundColor Green
        $alreadyInstalled++
    } else {
        Write-Host "Устанавливаю библиотеку: $library" -ForegroundColor Yellow
        pip install $library

        # Проверяем, успешно ли установлена библиотека
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Ошибка при установке библиотеки $library!" -ForegroundColor Red
            $failedLibraries += $library
        } else {
            $installedInSession++
        }
    }
}

# Итоговый отчёт
Write-Host "`nИтоговый отчёт:" -ForegroundColor Cyan
Write-Host "Требовалось установить библиотек: $totalLibraries" -ForegroundColor Cyan
Write-Host "Уже установлено до начала обработки: $alreadyInstalled" -ForegroundColor Cyan
Write-Host "Установлено в этом сеансе: $installedInSession" -ForegroundColor Cyan
Write-Host "Ошибки при установке: $($failedLibraries.Count)" -ForegroundColor Cyan

if ($failedLibraries.Count -gt 0) {
    Write-Host "Список библиотек с ошибками:" -ForegroundColor Red
    foreach ($failedLibrary in $failedLibraries) {
        Write-Host "- $failedLibrary" -ForegroundColor Red
    }
}

# Завершение логгирования
Stop-Transcript