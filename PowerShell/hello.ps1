Write-Host "Привет, мир!" -ForegroundColor Green
'one' -replace 'o', 't' `
-replace 'n', 'w' `
-replace 'e', 'o'
# Write-Host "`a"
# [Console]::Beep(400, 300)  # Частота 800 Гц, длительность 200 мс
# “Culture is $($host.CurrentCulture)”
# $host
$object = [PSCustomObject]@{
    Array = @(1, 2, 3, 4, 5)
}
# $object.Array
$object | ConvertTo-Json