param (
    [string]$Source = "D:\Library",              # Исходная папка
    [string]$Target = "E:\Backup\Library",       # Целевая папка
    [int]$Days = 7                               # Период в днях для поиска изменений
)

$threshold = (Get-Date).AddDays(-$Days)

Write-Host "Поиск изменённых подкаталогов в $Source за последние $Days дней..." -ForegroundColor Cyan

# Получаем все подкаталоги первого уровня
$subfolders = Get-ChildItem -Path $Source -Directory

foreach ($folder in $subfolders) {
    $fullPath = $folder.FullName

    # Определяем последнее время изменения внутри подкаталога
    $lastWrite = (Get-ChildItem -Path $fullPath -Recurse -File -ErrorAction SilentlyContinue | 
                  Sort-Object LastWriteTime -Descending | 
                  Select-Object -First 1).LastWriteTime

    if ($lastWrite -gt $threshold) {
        $dest = Join-Path -Path $Target -ChildPath $folder.Name

        Write-Host "🔄 Синхронизация: $fullPath → $dest (изменено: $lastWrite)" -ForegroundColor Green

        robocopy $fullPath $dest /MIR /NDL /NFL /NJH /NJS /NP /R:1 /W:1 | Out-Null
    } else {
        Write-Host "⏭ Без изменений: $fullPath (последнее изменение: $lastWrite)" -ForegroundColor DarkGray
    }
}

Write-Host "✅ Завершено." -ForegroundColor Cyan
