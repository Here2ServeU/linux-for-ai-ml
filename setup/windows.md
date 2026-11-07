# Windows · WSL (Windows Subsystem for Linux)

WSL runs a real Ubuntu inside Windows. It's built in and free.

**You need:** Windows 11, or Windows 10 version 2004 (build 19041) or newer,
admin rights, and about 2 GB of free disk.
No admin rights? Use [Codespaces](codespaces.md) instead.

> ⚠️ **Don't install Git or Python on Windows** for this course. Linux can't see
> programs installed there. Install them inside Linux (step 3 below).

## 1. Install Ubuntu

Right-click **Start → Terminal (Admin)** (or **Windows PowerShell (Admin)**) and run:

```powershell
wsl --install -d Ubuntu-24.04
```

Restart when asked.

## 2. First launch

Open **Ubuntu 24.04** from the Start menu. The first time, it asks you for a
**Linux username and password**. They're new and separate from your Windows
login. You won't see the password as you type. That's normal.

## 3. Get the course

In the Ubuntu window:

```bash
sudo apt update && sudo apt install -y git python3
cd ~
git clone https://github.com/Here2ServeU/linux-for-ai-ml
cd linux-for-ai-ml && bash setup/doctor.sh
```

Clone into `~` (your Linux home), **not** `/mnt/c/...`. Files on the Windows drive
are slow from Linux and have odd permissions. The doctor warns you if you do this.

## VS Code (optional)

Install VS Code on Windows (https://code.visualstudio.com) and add the **WSL**
extension. Then, inside Ubuntu, run:

```bash
cd ~/linux-for-ai-ml && code .
```

VS Code opens connected to Linux. Its terminal is your Ubuntu shell.

## Troubleshooting

| You see | Do this |
|---|---|
| `0x80370102` / "virtualization not enabled" | Turn on **Intel VT-x / AMD-V (SVM)** in your BIOS/UEFI settings, then reboot. Also enable **Virtual Machine Platform** under *Turn Windows features on or off*. |
| `wsl` is not recognized | Windows is too old. Run Windows Update, or use Codespaces. |
| `wsl --install` only prints help text | WSL is already installed. Run `wsl --install -d Ubuntu-24.04` or `wsl --update`. |
| Ubuntu says "WSL 1" or runs slowly | In PowerShell: `wsl --set-version Ubuntu-24.04 2` |
| Forgot your Linux password | PowerShell: `wsl -d Ubuntu-24.04 -u root`, then `passwd <your-linux-username>` |
| Doctor says `MINGW64` / Git Bash | You're in Git Bash, not Ubuntu. Open **Ubuntu 24.04** from the Start menu. |
| Work laptop blocks WSL | Use [Codespaces](codespaces.md). |

Guides: https://learn.microsoft.com/windows/wsl/install · https://documentation.ubuntu.com/wsl
