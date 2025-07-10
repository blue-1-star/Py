# function Save-ToDataFile {
#     param(
#         [Parameter(Mandatory=$true, ValueFromPipeline=$true)]
#         $Data,
        
#         [string]$FileNamePattern = "pathEntries_{0:dd}_{0:MM}.txt"
#         # [string]$FileNamePattern = "pathEntries_{0:ddMMyy}.txt"
#     )
    
#     # Получаем путь к директории исполняемого скрипта
#     # $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
#     # $cwd = Split-Path -Parent $MyInvocation.MyCommand.Path
    
#      # Получаем абсолютный путь к текущему исполняемому файлу скрипта
#     $scriptPath = $PSCommandPath
#     if (-not $scriptPath) {
#         throw "Скрипт должен быть запущен из файла (не интерактивно)."
#     }
#     $scriptDir = [System.IO.Path]::GetDirectoryName($scriptPath)



#     # # Получаем путь к директории исполняемого скрипта (если скрипт запущен из файла)
#     # if ($MyInvocation.MyCommand.Path) {
#     #     $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
#     # } else {
#     #     # Если скрипт запущен интерактивно, используем текущую директорию
#     #     $scriptDir = $PWD.Path
#     # }



#     # Формируем путь к подкаталогу Data
#     $dataDir = Join-Path -Path $scriptDir -ChildPath "Data"
    
#     # Создаем каталог если не существует
#     if (-not (Test-Path -Path $dataDir)) {
#         New-Item -ItemType Directory -Path $dataDir | Out-Null
#     }
    
#     # Формируем имя файла с датой
#     $currentDate = Get-Date
#     # $day = (Get-Date).Day
#     # $month = (Get-Date).Month
#     # $yearShort = (Get-Date).Year % 100  # 2024 → 24
#     # $fileName = "pathEntries_{0}_{1}.txt" -f $day, $yearShort
#     # $fileName = $FileNamePattern -f $currentDate.Day, $currentDate.Year
#     # $fileName = $FileNamePattern -f $currentDate  # Передаём ОБЪЕКТ даты целиком
#     # $fileName = $FileNamePattern -f $day, $yearShort  
#     $fileName = $FileNamePattern -f $currentDate
#     # $fileName = "pathEntries_{0}_{1}.txt" -f $day, $yearShort
#     # Полный путь к файлу
#     $filePath = Join-Path -Path $dataDir -ChildPath $fileName
    
#     # Запись данных
#     $Data | Out-File -FilePath $filePath -Encoding UTF8
    
#     Write-Host "Файл сохранен: $filePath" -ForegroundColor Green
#     return $filePath
# }

$pathEntries = $env:PATH -split ';' 
Save-ToDataFile -Data $pathEntries
