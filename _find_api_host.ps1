$harPath = 'c:\Users\plex\Desktop\www.solarkcloud.com.har'
$json = Get-Content $harPath -Raw | ConvertFrom-Json
$jsEntries = $json.log.entries | Where-Object { $_.request.url -match '/static/js/.*\.js' -and $_.response.content.text }
foreach ($e in $jsEntries) {
  $t = $e.response.content.text
  $patterns = @(
    'p2\.api\.solarkcloud\.com',
    'ecsprod-api-new',
    'api\.solarkcloud\.com',
    'mysolark\.com',
    '/oauth/token',
    'csp-web',
    'baseURL',
    'BASE_API'
  )
  $found = @()
  foreach ($p in $patterns) {
    $m = [regex]::Matches($t, ".{0,40}$p.{0,60}")
    if ($m.Count -gt 0) {
      $found += "PATTERN ${p} ($($m.Count) hits):"
      $m | Select-Object -First 3 | ForEach-Object {
        $found += "  $($_.Value -replace "`r|`n", ' ')"
      }
    }
  }
  if ($found.Count -gt 0) {
    Write-Output "==== $($e.request.url.Split('/')[-1]) ===="
    $found | ForEach-Object { Write-Output $_ }
  }
}

$idx = (Invoke-WebRequest -Uri 'https://www.solarkcloud.com/' -UseBasicParsing -TimeoutSec 20).Content
Write-Output ''
Write-Output '==== INDEX SCRIPT TAGS ===='
[regex]::Matches($idx, 'src="[^"]+\.js[^"]*"') | ForEach-Object { $_.Value }

$mainJs = [regex]::Matches($idx, '/static/js/[^"]+\.js') | ForEach-Object { $_.Value } | Sort-Object -Unique
Write-Output ''
Write-Output 'Main JS from index:'
$mainJs | ForEach-Object { Write-Output $_ }

foreach ($path in $mainJs) {
  $url = "https://www.solarkcloud.com$path"
  try {
    $js = (Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 30).Content
    Write-Output "Fetched $path len=$($js.Length)"
    foreach ($p in @('p2\.api\.solarkcloud\.com', 'ecsprod', 'api\.solarkcloud\.com', '/oauth/token', 'csp-web', 'baseURL')) {
      $m = [regex]::Matches($js, ".{0,50}$p.{0,80}")
      if ($m.Count -gt 0) {
        Write-Output "PATTERN ${p}:"
        $m | Select-Object -First 5 | ForEach-Object {
          Write-Output ("  " + ($_.Value -replace "`r|`n", ' '))
        }
      }
    }
  } catch {
    Write-Output "fail $path : $($_.Exception.Message)"
  }
}
