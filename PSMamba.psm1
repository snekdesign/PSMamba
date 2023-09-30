Add-Type -Path "$PSScriptRoot\PSMamba.dll"

function Enter-MambaEnvironment (
    [ValidateNotNullOrEmpty()][String]$Name = 'base',
    [switch]$Stack
) {
    [Mamba]::Activate($Name, $Stack) | Invoke-Expression
}

function Exit-MambaEnvironment {
    [Mamba]::Deactivate() | Invoke-Expression
}

Set-Alias etenv Enter-MambaEnvironment
Set-Alias exenv Exit-MambaEnvironment
Export-ModuleMember -Function * -Alias *
