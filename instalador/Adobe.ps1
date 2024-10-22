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
    "$timestamp - $Message" | Out-File -FilePath $logFile -Append -Encoding UTF8
}

# Criar diretório temporário
$tempDir = "C:\Programas-Ultra"
if (-Not (Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir | Out-Null
}

# URL do instalador
$Url = "https://fs01.ultra.com.vc/s/YW977GjgGQ2woo3/download?path=%2F&files=Adobe%20Reader%20Pt-BR.exe"
$Nome = "Adobe_Reader_Pt-BR.exe"
$InstallerPath = Join-Path -Path $tempDir -ChildPath $Nome

try {
    Invoke-WebRequest -Uri $Url -OutFile $InstallerPath
    Log-Message "Download do $Nome concluído."

    # Instalando com parâmetros adequados
    $installArgs = "/sAll /slf /re /msi DISABLE_FIU_CHECK=1 TRANSITION_INSTALL_MODE=3 EULA_ACCEPT=YES"
    $process = Start-Process -FilePath $InstallerPath -ArgumentList $installArgs -Wait -NoNewWindow -PassThru
    
    # Verifica o código de saída
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
