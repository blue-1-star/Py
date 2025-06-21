# Получаем текущий PATH и разбиваем на части
$pathEntries = $env:PATH -split ';'

# Фильтруем и обрабатываем записи
$cleanPath = $pathEntries | Where-Object {
    $_ -ne '' -and           # Удаляем пустые
    $_ -notmatch '^%' -and   # Удаляем переменные среды вроде %PATH%
    $_ -notmatch '\\$'       # Удаляем пути, заканчивающиеся на \
} | ForEach-Object {
    # Нормализуем пути (убираем слеши в конце)
    $_.TrimEnd('\')
} | Select-Object -Unique    # Оставляем только уникальные

# Формируем новый PATH
$newPath = ($cleanPath -join ';').Trim(';')

# Показываем статистику
Write-Host "Было элементов: $($pathEntries.Count)"
Write-Host "Стало элементов: $($cleanPath.Count)"
Write-Host "Удалено дубликатов: $($pathEntries.Count - $cleanPath.Count)"

# Записываем в файл для проверки
$cleanPath | Out-File -FilePath "$env:USERPROFILE\path_clean.txt" -Encoding UTF8

# Предложение применить изменения
Write-Host "`nНовый PATH готов к применению."
$apply = Read-Host "Применить изменения? (Y/N)"
if ($apply -eq 'Y') {
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "Machine")
    Write-Host "PATH успешно обновлен! Закройте и снова откройте терминал."
} else {
    Write-Host "Изменения не применены. Проверьте файл path_clean.txt"
}