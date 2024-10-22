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

# Definir o nome do arquivo e o caminho para extração
$Url = "https://fs01.ultra.com.vc/s/YW977GjgGQ2woo3/download?path=%2F&files=DesignReview-2017_PT-BR.exe"
$Nome = "DesignReview-2017_PT-BR.exe"
$InstallerPath = Join-Path -Path $tempDir -ChildPath $Nome
$extractPath = "C:\Autodesk\SetupDesignReview"

try {
    Invoke-WebRequest -Uri $Url -OutFile $InstallerPath
    Log-Message "Download do $Nome concluído."

    # Verifica se o 7-Zip está instalado para a extração
    $sevenZipPath = "C:\Program Files\7-Zip\7z.exe"
    if (-Not (Test-Path $sevenZipPath)) {
        Log-Message "7-Zip não está instalado. Por favor, instale 7-Zip para continuar."
        exit
    }

    # Criar o diretório de extração se não existir
    if (-Not (Test-Path $extractPath)) {
        New-Item -ItemType Directory -Path $extractPath | Out-Null
    }

    # Extrai o conteúdo do instalador para o diretório específico
    & $sevenZipPath x $InstallerPath -o"$extractPath" -aoa
    Log-Message "Extração do $Nome concluída."

    # Verifica se o arquivo MSI está presente
    $msiPath = Join-Path -Path $extractPath -ChildPath "x86\ADR\SetupDesignReview.msi"
    if (-Not (Test-Path $msiPath)) {
        Log-Message "SetupDesignReview.msi não encontrado em $extractPath. Arquivos extraídos:"
        Get-ChildItem -Path $extractPath -Recurse | ForEach-Object { Log-Message $_.FullName }
        exit
    }

    # Instalação silenciosa usando o arquivo MSI
    Start-Process -FilePath "msiexec.exe" -ArgumentList "/i", "`"$msiPath`"", "ADSK_DESKTOPSHORTCUT_1=1", "/quiet", "/log", "$env:TEMP\ADR_log.log" -Wait -NoNewWindow
    Log-Message "Instalação do Design Review concluída com sucesso!"

    # Remover instalador
    Remove-Item -Path $InstallerPath -Force
    Log-Message "Instalador de $Nome removido."
} catch {
    Log-Message "Erro: $_"
}
