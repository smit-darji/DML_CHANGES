# Read the content of the pom.xml to extract the original module order
$pomContent = Get-Content -Path $FILE
$pomModules = @()
$inModulesSection = $false
$insideCommentBlock = $false
foreach ($line in $pomContent) {
    # Check for start and end of <modules> section
    if ($line -match '<modules>') {
        $inModulesSection = $true
        continue
    }
    if ($line -match '</modules>') {
        $inModulesSection = $false
        continue
    }
  
    # Skip commented lines
    if ($line -match '<!--') { $insideCommentBlock = $true }
    if ($line -match '-->') { $insideCommentBlock = $false; continue }
  
    # Process only if we are inside the <modules> section and the line is not part of a comment
    if ($inModulesSection -and -not $insideCommentBlock -and $line -match '<module>(.*)</module>') {
        $module = $matches[1].Trim()
        $pomModules += $module
    }
}
# Display or further process the extracted modules
Write-Host "Extracted pommodules: $($pomModules -join ', ')"
Write-Host "----------------------------------------------------------------------------------"
$pomModules = $pomModules | ForEach-Object { $_ -replace '/', '\' }
# Assuming $MODULES is the list of changed files' DB schemas
# Assuming $pomModules is the list of DB schemas from the pom.xml
$missingModules = @()
# Loop through each module in $MODULES to check if it's in the $pomModules array
foreach ($module in $MODULES) {
    if (-not ($pomModules -contains $module)) {
        $missingModules += $module
    }
}

$missingModules = $missingModules | ForEach-Object { $_ -replace '\\', '/' }
# If there are missing modules, throw an error
if ($missingModules.Count -gt 0) {
    Write-Host "Error: The following DB schemas are present in MODULES but missing in pom.xml:"
    Write-Host "$($missingModules -join ', ')"
    throw "Missing schemas detected: $($missingModules -join ', ')"
    exit
} else {
    Write-Host "All modules are present in the pom.xml content."
}
# Reorder the filtered modules based on the order in pom.xml
$orderedModules = @()
$orderedModules = $MODULES | Sort-Object { $pomModules.IndexOf($_)}

$ordered_Modules = $orderedModules | ForEach-Object { $_ -replace '\\', '/' }
Write-Host "Ordered Modules: $($ordered_Modules -join ',')"
# Generate new content for the <modules> section in the pom.xml
$newContent = @()
$inModules = $false
foreach ($line in $pomContent) {
  if ($line -match '<modules>') {
    $inModules = $true
    $newContent += $line
    # Add the modules in the reordered list
    foreach ($module in $orderedModules) {
      $newContent += "<module>$module</module>"
    }
    continue
  }
  if ($line -match '</modules>') {
    $inModules = $false
    $newContent += $line
    continue
  }
  if (-not $inModules) {
    $newContent += $line
  }
}
# Write the new content back to the file
Set-Content -Path $FILE -Value $newContent