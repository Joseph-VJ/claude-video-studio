$ErrorActionPreference='Stop'
. 'E:\Video\scripts\env.ps1'
$env:CONCAT_MCP_ROOTS='E:\Video'
$env:XDG_CONFIG_HOME='E:\Video\cache\config'
$env:XDG_DATA_HOME='E:\Video\cache\data'
& 'E:\Video\tools\Concat-0.2.8\concat.exe' --mcp headless
exit $LASTEXITCODE
