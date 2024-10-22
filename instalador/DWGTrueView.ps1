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

# Configurações de log
$logFile = "C:\Programas-Ultra\instalacao-log.txt"

function Log-Message {
    param ([string]$Message)
    $timestamp = (Get-Date).ToString("dd-MM-yyyy HH:mm:ss")
    "$timestamp - $Message" | Out-File -FilePath $logFile -Append -Encoding UTF8
}

# Criar diretório temporário
$tempDir = "C:\Programas-Ultra"
if (-Not (Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir | Out-Null
}

# URL do instalador
$Url = "https://fs01.ultra.com.vc/s/YW977GjgGQ2woo3/download?path=%2F&files=DWGTrueView_2025_English_64bit_dlm.sfx.exe"
$Nome = "Create_Installer_PLC0000037_202x_English_WIN64.exe"
$InstallerPath = Join-Path -Path $tempDir -ChildPath $Nome


try {
    # Download do instalador
    Invoke-WebRequest -Uri $Url -OutFile $InstallerPath
    Log-Message "Download do $Nome concluído."

    # Executar o instalador para baixar os arquivos necessários
    Start-Process -FilePath $InstallerPath -ArgumentList "-q" -Wait
    Log-Message "Download dos arquivos de instalação concluído."

    # Caminho para os arquivos de instalação
    $extractedPath = Join-Path -Path "$env:USERPROFILE\Downloads\Autodesk" -ChildPath "DWG TrueView 2025 - English - (EN)"
    
    # Verifica se a pasta de extração existe
    if (Test-Path $extractedPath) {
        Log-Message "A pasta de instalação encontrada em: $extractedPath"
        
        # Instalando usando o Setup.exe
        $setupExePath = Join-Path -Path $extractedPath -ChildPath "Setup.exe"
        if (Test-Path $setupExePath) {
            Start-Process -FilePath $setupExePath -ArgumentList "--silent","ADSK_DESKTOPSHORTCUT_1=1" -Wait
            Log-Message "Instalação do DWG TrueView concluída com sucesso!"
        } else {
            Log-Message "Arquivo Setup.exe não encontrado em $extractedPath."
        }
    } else {
        Log-Message "A pasta de instalação não foi encontrada em $extractedPath. Verifique o caminho e a versão do DWG TrueView."
        exit
    }

    # Remover instalador
    Remove-Item -Path $InstallerPath -Force
    Log-Message "Instalador de $Nome removido."
} catch {
    Log-Message "Erro: $_"
}