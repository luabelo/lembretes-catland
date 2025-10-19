$scriptPath = Get-Location
$pythonPath = (Get-Command python).Source
$mainScript = Join-Path $scriptPath "src\main.py"

$action = New-ScheduledTaskAction -Execute $pythonPath -Argument $mainScript -WorkingDirectory $scriptPath
$trigger = New-ScheduledTaskTrigger -Daily -At 6:00AM
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

$taskName = "Catland - Sistema de Lembretes"

$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "Tarefa existente removida."
}

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "Envia lembretes automáticos para coordenação de atendimentos da ONG Catland"

Write-Host "Tarefa agendada criada com sucesso!"
Write-Host "Nome: $taskName"
Write-Host "Horário: Diariamente às 06:00"
Write-Host "Script: $mainScript"
