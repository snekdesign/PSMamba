# PSMamba
[![][1]][2] [![][3]][4]
Call [libmamba][5] directly from (Windows) PowerShell via C++/CLI.
Say goodbye to `libmambapy`, `mamba` and `micromamba`.
## Installation
```powershell
boa build --pkg-format=2 .
micromamba install -c $Env:MAMBA_ROOT_PREFIX\conda-bld psmamba
```
## Usage
```powershell
Import-Module $Env:MAMBA_ROOT_PREFIX\Library\bin\PSMamba.psm1
Get-Help etenv
Get-Help exenv
```

[1]: https://img.shields.io/badge/license-GPL--2.0--only-blue.svg
[2]: https://github.com/snekdesign/PSMamba/blob/main/LICENSE#L1-L339
[3]: https://img.shields.io/badge/license-Anti--996-blue.svg
[4]: https://github.com/snekdesign/PSMamba/blob/main/LICENSE#L343-L388
[5]: https://github.com/mamba-org/mamba/tree/main/libmamba
