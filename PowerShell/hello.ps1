function Save-ToDataFile {
    param(
        [Parameter(Mandatory=$true, ValueFromPipeline=$true)]
        $Data,
        
        [string]$FileNamePattern = "pathEntries_{0:dd}_{1:yy}.txt"
    )
    
    # Получаем путь к директории исполняемого скрипта
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
    
    # Формируем путь к подкаталогу Data
    $dataDir = Join-Path -Path $scriptDir -ChildPath "Data"
    
    # Создаем каталог если не существует
    if (-not (Test-Path -Path $dataDir)) {
        New-Item -ItemType Directory -Path $dataDir | Out-Null
    }
    
    # Формируем имя файла с датой
    $currentDate = Get-Date
    $fileName = $FileNamePattern -f $currentDate.Day, $currentDate.Year
    
    # Полный путь к файлу
    $filePath = Join-Path -Path $dataDir -ChildPath $fileName
    
    # Запись данных
    $Data | Out-File -FilePath $filePath -Encoding UTF8
    
    return $filePath
}
Write-Host "Привет, мир!" -ForegroundColor Green
'one' -replace 'o', 't' `
-replace 'n', 'w' `
-replace 'e', 'o'
# Write-Host "`a"
# [Console]::Beep(400, 300)  # Частота 800 Гц, длительность 200 мс
# “Culture is $($host.CurrentCulture)”
# $host
#$object = [PSCustomObject]@{
#    Array = @(1, 2, 3, 4, 5)
#}
# $object.Array
# $object | ConvertTo-Json
$cwd = Split-Path -Parent $MyInvocation.MyCommand.Path
#Write-Host "Current work directory: ... ", $cwd
$pathEntries = $env:PATH -split ';'  

 # Получаем путь к директории исполняемого скрипта
# $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition 
    # Формируем путь к подкаталогу Data
$dataDir = Join-Path -Path $cwd -ChildPath "Data"
# Убедимся, что подкаталог Data существует (если нет - создадим)

# $dataDir = Join-Path -Path (Get-Location) -ChildPath "Data"
if (-not (Test-Path -Path $dataDir)) {
    New-Item -ItemType Directory -Path $dataDir | Out-Null
}

# Полный путь к файлу
$filePath = Join-Path -Path $dataDir -ChildPath "pathEntries.txt"
Write-Host $filePath
# Записываем содержимое переменной в файл (перезапись)
# $pathEntries | Out-File -FilePath $filePath -Encoding UTF8

# Альтернативный вариант (более лаконичный):
Set-Content -Path $filePath -Value $pathEntries -Encoding UTF8
Save-ToDataFile -Data "Data" 

Write-Host "Было элементов: $($pathEntries.Count)"
