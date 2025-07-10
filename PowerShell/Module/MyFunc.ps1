$global:__MyFuncScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
function Save-ToDataFile {
    param(
        [Parameter(Mandatory=$true, ValueFromPipeline=$true)]
        $Data,
        
        [string]$FileNamePattern = "pathEntries_{0:dd}_{1:MM}.txt"
    )
    
    # Получаем путь к директории исполняемого скрипта
    # $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
    
    # Формируем путь к подкаталогу Data
    $dataDir = Join-Path -Path $global:__MyFuncScriptDir -ChildPath "Data"
    
    # Создаем каталог если не существует
    if (-not (Test-Path -Path $dataDir)) {
        New-Item -ItemType Directory -Path $dataDir | Out-Null
    }
    
    # Формируем имя файла с датой
    $currentDate = Get-Date
    $fileName = $FileNamePattern -f $currentDate, $currentDate
    
    # Полный путь к файлу
    $filePath = Join-Path -Path $dataDir -ChildPath $fileName
    
    # Запись данных
    $Data | Out-File -FilePath $filePath -Encoding UTF8
    
    return $filePath
}

# function Clean-PathVariable {
#     param (
#         [ValidateSet("User", "Machine")]
#         [string]$Scope = "User",

#         [switch]$PreviewOnly
#     )

#     Write-Host "`n🧼 Starting PATH cleanup for scope: $Scope" -ForegroundColor Cyan

#     # Каталог Data
#     $dataDir = Join-Path $global:__MyFuncScriptDir "Data"
#     if (-not (Test-Path $dataDir)) {
#         New-Item -ItemType Directory -Path $dataDir | Out-Null
#     }

#     # Получение PATH
#     $rawPath = [Environment]::GetEnvironmentVariable("Path", $Scope)
#     $entries = $rawPath -split ";" | ForEach-Object { $_.Trim() }

#     # Фильтрация
#     $nonEmpty = $entries | Where-Object { $_.Trim() -ne "" }
#     $normalized = $nonEmpty | ForEach-Object { $_.Trim().ToLower() }
#     $unique = $normalized | Sort-Object -Unique

#     # Хеш-таблица: нормализованный путь → оригинальный
# $seen = @{}
# $uniqueOriginal = @()

# foreach ($entry in $nonEmpty) {
#     $key = $entry.Trim().ToLower()
#     if (-not $seen.ContainsKey($key)) {
#         $seen[$key] = $true
#         $uniqueOriginal += $entry
#     }
# }


#     $valid = $unique | Where-Object { Test-Path $_ }

#     # Диагностика
#     $removedEmpty = $entries.Count - $nonEmpty.Count
#     $removedDuplicates = $nonEmpty.Count - $unique.Count
#     $removedInvalid = $unique.Count - $valid.Count

#     $invalidPaths = $unique | Where-Object { -not (Test-Path $_) }
#     $removedPaths = @()
#     $removedPaths += ($entries | Where-Object { $_ -eq "" })
#     $removedPaths += ($nonEmpty | Group-Object | Where-Object { $_.Count -gt 1 } | ForEach-Object { $_.Group[1..($_.Count - 1)] })
#     $removedPaths += $invalidPaths
#     $removedPaths = $removedPaths | Sort-Object -Unique

#     # Лог-файлы
#     $timestamp = (Get-Date -Format "yyyyMMdd_HHmmss")
#     $baseName = "path_$Scope`_$timestamp"
#     $backupPath = Join-Path $dataDir "$baseName`_backup.txt"
#     $removedLogPath = Join-Path $dataDir "$baseName`_removed.txt"
#     $csvReportPath = Join-Path $dataDir "$baseName`_report.csv"

#     # Сохранение бэкапа
#     $entries -join "`r`n" | Set-Content $backupPath
#     Write-Host "💾 Backup saved to: $backupPath"

#     # Сохранение удалённых путей
#     if ($removedPaths.Count -gt 0) {
#         $removedPaths -join "`r`n" | Set-Content $removedLogPath
#         Write-Host "🧹 Removed paths saved to: $removedLogPath"
#     }

#     # CSV отчёт
#     $report = [System.Collections.Generic.List[PSCustomObject]]::new()
#     foreach ($item in $entries) {
#         $status = switch ($true) {
#     { [string]::IsNullOrWhiteSpace($item) } { "Empty"; break }
#     { $invalidPaths -contains $item }       { "Invalid"; break }
#     { $valid -contains $item }              { "Valid"; break }
#     default                                 { "Duplicate" }
# }
#         $report.Add([PSCustomObject]@{
#             Path   = $item
#             Status = $status
#         })
#     }
#     $report | Export-Csv -Path $csvReportPath -NoTypeInformation -Encoding UTF8
#     Write-Host "📊 Report saved to: $csvReportPath"

#     # Итоги
#     Write-Host "`n🔍 Total entries: $($entries.Count)"
#     Write-Host "🧹 Removed empty: $removedEmpty"
#     Write-Host "🧹 Removed duplicates: $removedDuplicates"
#     Write-Host "🧹 Removed invalid: $removedInvalid"

#     # Предпросмотр или запись
#     if ($PreviewOnly) {
#         Write-Host "`n🔎 Preview only — PATH was not modified." -ForegroundColor Yellow
#     } else {
#         $cleanedPath = $valid -join ";"
#         [Environment]::SetEnvironmentVariable("Path", $cleanedPath, $Scope)
#         Write-Host "`n✅ Cleaned PATH has been set for scope: $Scope" -ForegroundColor Green
#     }
# }

function Clean-PathVariable {
    param (
        [switch]$Update
    )

    $entries = $env:PATH -split ';'

    # Удаляем пустые строки
    $nonEmpty = $entries | Where-Object { $_.Trim() -ne "" }

    # Удаляем дубликаты (Trim + ToLower), но сохраняем оригиналы
    $seen = @{}
    $unique = @()
    foreach ($entry in $nonEmpty) {
        $key = $entry.Trim().ToLower()
        if (-not $seen.ContainsKey($key)) {
            $seen[$key] = $true
            $unique += $entry
        }
    }

    # Классифицируем пути
    $valid = @()
    $invalid = @()
    foreach ($item in $unique) {
        if (Test-Path $item) {
            $valid += $item
        } else {
            $invalid += $item
        }
    }

    # Готовим лог
    $logEntries = foreach ($item in $entries) {
        # $trimmed = $item.Trim()
        $status = if ([string]::IsNullOrWhiteSpace($item)) {
            "Empty"
        } elseif ($invalid -contains $item) {
            "Invalid"
        } elseif ($valid -contains $item) {
            "Valid"
        } else {
            "Duplicate"
        }

        [PSCustomObject]@{
            Path   = $item
            Status = $status
        }
    }

    # Сохраняем лог в Data-подкаталог
    $dataDir = Join-Path $global:__MyFuncScriptDir "Data"
    if (-not (Test-Path $dataDir)) {
        New-Item -ItemType Directory -Path $dataDir | Out-Null
    }

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $logPath = Join-Path $dataDir "CleanPathLog_$timestamp.csv"

    $logEntries | Export-Csv -Path $logPath -NoTypeInformation -Encoding UTF8
    Write-Host "Path log saved to: $logPath"

    # Если задано -Update, перезаписать переменную PATH
    if ($Update) {
        $env:PATH = ($valid -join ';')
        Write-Host "Environment variable PATH has been updated."
    }
}

function Repair-PathVariable {
    param (
        [switch]$Update
    )

    $entries = $env:PATH -split ';'

    $totalCount = $entries.Count
    $emptyCount = ($entries | Where-Object { [string]::IsNullOrWhiteSpace($_) }).Count

    # Удаляем пустые строки
    $nonEmpty = $entries | Where-Object { $_.Trim() -ne "" }

    # Удаляем дубликаты (Trim + ToLower), но сохраняем оригиналы
    $seen = @{}
    $unique = @()
    foreach ($entry in $nonEmpty) {
        $key = $entry.Trim().ToLower()
        if (-not $seen.ContainsKey($key)) {
            $seen[$key] = $true
            $unique += $entry
        }
    }

    $duplicateCount = $nonEmpty.Count - $unique.Count

    # Классифицируем пути
    $valid = @()
    $invalid = @()

    foreach ($item in $unique) {
        if (Test-Path $item) {
            $valid += $item
        } else {
            $invalid += $item
        }
    }

    $invalidCount = $invalid.Count
    $validCount = $valid.Count

    # Готовим лог
    $logEntries = foreach ($item in $entries) {
        $status = if ([string]::IsNullOrWhiteSpace($item)) {
            "Empty"
        } elseif ($invalid -contains $item) {
            "Invalid"
        } elseif ($valid -contains $item) {
            "Valid"
        } else {
            "Duplicate"
        }

        [PSCustomObject]@{
            Path   = $item
            Status = $status
        }
    }

    # Сохраняем лог
    $dataDir = Join-Path $global:__MyFuncScriptDir "Data"
    if (-not (Test-Path $dataDir)) {
        New-Item -ItemType Directory -Path $dataDir | Out-Null
    }

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $logPath = Join-Path $dataDir "RepairPathLog_$timestamp.csv"

    $logEntries | Export-Csv -Path $logPath -NoTypeInformation -Encoding UTF8

    # Вывод статистики
    Write-Host ""
    Write-Host "Path repair summary:" -ForegroundColor Cyan
    Write-Host "  Total entries:         $totalCount"
    Write-Host "  Empty entries removed: $emptyCount"
    Write-Host "  Duplicate entries:     $duplicateCount"
    Write-Host "  Invalid paths:         $invalidCount"
    Write-Host "  Valid entries:         $validCount"
    Write-Host ""
    Write-Host "Log saved to: $logPath" -ForegroundColor DarkGray

    # Обновляем переменную PATH (если указано)
    if ($Update) {
        $env:PATH = ($valid -join ';')
        Write-Host "`$env:PATH has been updated." -ForegroundColor Yellow
    }
    # Перманентное сохранение в User PATH
    if ($Persist) {
        $newPath = ($valid -join ';')

     # Резервная копия текущего User PATH
        $backupFile = Join-Path $dataDir "BackupPath_User_$timestamp.txt"
        $originalUserPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        $originalUserPath | Out-File -FilePath $backupFile -Encoding UTF8
        Write-Host "Backup of user PATH saved to: $backupFile" -ForegroundColor DarkGray
        
        # Подтверждение от пользователя
        $confirm = Read-Host "Do you want to permanently update User PATH with the cleaned version? (Y/N)"
        if ($confirm -match '^[Yy]') {
            [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
            Write-Host "User PATH has been permanently updated." -ForegroundColor Green
        } else {
            Write-Host "Persisting cancelled by user." -ForegroundColor DarkYellow
        }
    }
}



function Get-SystemInfo {
    Get-ComputerInfo
}
function func1 {   
    Write-Host "Test func1"
    
}