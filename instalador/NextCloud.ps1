# Função para reiniciar o script com privilégios administrativos
function Start-ProcessAsAdmin {
    $arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$($MyInvocation.MyCommand.Path)`""
    Start-Process powershell -ArgumentList $arguments -Verb RunAs
    exit
}

# Verifica se o script está sendo executado como administrador
if (-Not ([Security.Principal.WindowsIdentity]::GetCurrent().Groups -match "S-1-5-32-544")) {
    Start-ProcessAsAdmin
}

$logFile = "C:\Programas-Ultra\instalacao-log.txt"

function Log-Message {
    param ([string]$Message)
    $timestamp = (Get-Date).ToString("dd-MM-yyyy HH:mm:ss")
    $logEntry = "$timestamp - $Message"
    
    # Escreve no log
    $logEntry | Out-File -FilePath $logFile -Append -Encoding UTF8
    # Escreve no console
    Write-Host $logEntry
}

# Criar diretório temporário
$tempDir = "C:\Programas-Ultra"
if (-Not (Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir | Out-Null
}

# Testando o download de um arquivo
$Url = "https://fs01.ultra.com.vc/s/YW977GjgGQ2woo3/download?path=%2F&files=Nextcloud-3.13.2-x64.msi"
$Nome = "Nextcloud-3.13.2-x64.msi"
$InstallerPath = Join-Path -Path $tempDir -ChildPath $Nome

try {
    Invoke-WebRequest -Uri $Url -OutFile $InstallerPath
    Log-Message "Download do $Nome concluído."

    # Instalando
    Start-Process -FilePath "msiexec.exe" -ArgumentList "/passive", "/i", "$InstallerPath", "ADDDEFAULT=DesktopShortcut", "REBOOT=ReallySuppress", "SKIPAUTOUPDATE=3", "LAUNCH=1" -Wait -NoNewWindow
    Log-Message "Instalação do $Nome concluída com sucesso!"
    
    # Remover instalador
    Remove-Item -Path $InstallerPath -Force
    Log-Message "Instalador de $Nome removido."
} catch {
    Log-Message "Erro: $_"
}
