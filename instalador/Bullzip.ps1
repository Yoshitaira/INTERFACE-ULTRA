# Função para reiniciar o script com privilégios administrativos
function Start-ProcessAsAdmin {
    # Cria um novo processo PowerShell com os mesmos argumentos
    $arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$($MyInvocation.MyCommand.Path)`""
    Start-Process powershell -ArgumentList $arguments -Verb RunAs
    exit
}

# Verifica se o script está sendo executado como administrador
if (-Not ([Security.Principal.WindowsIdentity]::GetCurrent().Groups -match "S-1-5-32-544")) {
    Start-ProcessAsAdmin
}

# O restante do código só executa se o script já estiver elevado
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

# Testando o download de um arquivo
$Url = "https://fs01.ultra.com.vc/s/YW977GjgGQ2woo3/download?path=%2F&files=BullzipPDFPrinter_14_4_0_2963.exe"
$Nome = "BullzipPDFPrinter_14_4_0_2963.exe"
$InstallerPath = Join-Path -Path $tempDir -ChildPath $Nome

try {
    Invoke-WebRequest -Uri $Url -OutFile $InstallerPath
    Log-Message "Download do $Nome concluído."

    # Instalando
    $installArgs = "/SP- /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /ACCEPT_EULA"
    $process = Start-Process -FilePath $InstallerPath -ArgumentList $installArgs -Wait -NoNewWindow -PassThru

    if ($process.ExitCode -eq 0) {
        Log-Message "Instalação do $Nome concluída com sucesso!"
    } else {
        Log-Message "Erro na instalação de $Nome. Código de saída: $($process.ExitCode)"
    }
    
    # Remover instalador
    Remove-Item -Path $InstallerPath -Force
    Log-Message "Instalador de $Nome removido."
} catch {
    Log-Message "Erro: $_"
}
