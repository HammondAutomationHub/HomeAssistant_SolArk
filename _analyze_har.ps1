$harPath = 'c:\Users\plex\Desktop\www.solarkcloud.com.har'
$json = Get-Content $harPath -Raw | ConvertFrom-Json
Write-Output "Entries: $($json.log.entries.Count)"
Write-Output "Started: $($json.log.pages[0].startedDateTime)"
Write-Output ""
Write-Output "=== API-ish URLs ==="
$json.log.entries | ForEach-Object {
    $url = $_.request.url
    if ($url -match 'api|oauth|login|token|auth|plant|inverter|energy|realtime|flow|device') {
        $method = $_.request.method
        $status = $_.response.status
        $mime = $_.response.content.mimeType
        $size = $_.response.content.size
        Write-Output "$method $status [$mime size=$size] $url"
    }
} | Select-Object -First 120
