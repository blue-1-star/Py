# Скрипт для получения конфигурации ПК
function Get-SystemInfo {
    Write-Host "`n=== Конфигурация ПК ===`n" -ForegroundColor Cyan

    # 1. Информация о системе
    $os = Get-CimInstance Win32_OperatingSystem
    $cpu = Get-CimInstance Win32_Processor
    $bios = Get-CimInstance Win32_BIOS
    $ram = Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum

    Write-Host "### Основная информация ###" -ForegroundColor Green
    Write-Host "ОС: $($os.Caption) ($($os.OSArchitecture))"
    # Write-Host "Версия BIOS: $($bios.SMBIOSBIOSVersion) (Дата: $($bios.ReleaseDate.ToString('yyyy-MM-dd')))"
    # Write-Host "Версия BIOS: $($bios.SMBIOSBIOSVersion)`
    # (Дата: $($bios.ReleaseDate.ToString('yyyy-MM-dd')))"
    $biosDate = $bios.ReleaseDate.ToString('yyyy-MM-dd')
    Write-Host "Версия BIOS: $($bios.SMBIOSBIOSVersion) (Дата: $biosDate)"
    Write-Host "Производитель: $($bios.Manufacturer)`n"

    # 2. Процессор
    Write-Host "### Процессор ###" -ForegroundColor Green
    Write-Host "Модель: $($cpu.Name)"
    Write-Host "Ядер: $($cpu.NumberOfCores), Потоков: $($cpu.NumberOfLogicalProcessors)"
    Write-Host "Тактовая частота: $([math]::Round($cpu.MaxClockSpeed/1000, 2)) GHz`n"

    # 3. Оперативная память
    Write-Host "### Оперативная память ###" -ForegroundColor Green
    Write-Host "Всего ОЗУ: $([math]::Round($ram.Sum/1GB, 2)) GB"
    Get-CimInstance Win32_PhysicalMemory | ForEach-Object {
        Write-Host "- $([math]::Round($_.Capacity/1GB, 2)) GB $($_.Speed) MHz ($($_.Manufacturer) $($_.PartNumber))"
    }
    Write-Host ""

    # 4. Видеокарта
    Write-Host "### Графика ###" -ForegroundColor Green
    $gpus = Get-CimInstance Win32_VideoController
    if ($gpus.Count -eq 0) {
        Write-Host "Видеокарта не обнаружена"
    } else {
        $gpus | ForEach-Object {
            Write-Host "Видеокарта: $($_.Name)"
            Write-Host "VRAM: $([math]::Round($_.AdapterRAM/1GB, 2)) GB"
            Write-Host "Драйвер: $($_.DriverVersion)`n"
        }
    }

    # 5. Диски
    Write-Host "### Накопители ###" -ForegroundColor Green
    Get-CimInstance Win32_DiskDrive | ForEach-Object {
        $sizeGB = [math]::Round($_.Size/1GB, 2)
        Write-Host "$($_.Model) - $sizeGB GB (Serial: $($_.SerialNumber.Trim()))"
    }
    Write-Host ""

    # 6. Сеть
    Write-Host "### Сетевые адаптеры ###" -ForegroundColor Green
    Get-CimInstance Win32_NetworkAdapter | Where-Object {
        $_.NetEnabled -eq $true -and $_.PhysicalAdapter -eq $true
    } | ForEach-Object {
        Write-Host "$($_.Name) (MAC: $($_.MACAddress))"
    }
}

# Выполняем функцию
Get-SystemInfo

# Дополнительно: сохраняем в файл
$outputPath = "$env:USERPROFILE\Desktop\PC_Configuration.txt"
Get-SystemInfo | Out-File -FilePath $outputPath -Encoding UTF8
Write-Host "`nОтчёт сохранён в: $outputPath" -ForegroundColor Yellow