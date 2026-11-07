# Mac · Multipass

Multipass runs a small Ubuntu virtual machine on your Mac with one command. It
works on Apple Silicon (M1-M4) and Intel Macs.

**You need:** macOS 13 or newer, admin rights, and about 5 GB of free disk.

> ⚠️ **Don't install Git or Python on macOS** for this course. Linux can't see
> programs installed there. Install them inside Linux (step 3 below).
> The macOS Terminal alone won't pass the doctor either: macOS isn't Linux
> (its `sed`, `du` and `find` behave differently).

## 1. Install Multipass

With Homebrew (https://brew.sh), run this in **Terminal**:

```bash
brew install --cask multipass
```

No Homebrew? Download the installer from https://canonical.com/multipass/install.

## 2. Create and enter your Linux VM

```bash
multipass launch 24.04 --name ailab --disk 10G --memory 2G
multipass shell ailab
```

Your prompt changes to `ubuntu@ailab:~$`. You're now in Linux.

## 3. Get the course (inside the VM)

```bash
sudo apt update && sudo apt install -y git python3
git clone https://github.com/Here2ServeU/linux-for-ai-ml
cd linux-for-ai-ml && bash setup/doctor.sh
```

## Daily use

| To | Run (in macOS Terminal) |
|---|---|
| Get back in | `multipass shell ailab` |
| Pause it (frees memory) | `multipass stop ailab` |
| See what's running | `multipass list` |
| Start over from scratch | `multipass delete --purge ailab`, then step 2 again |

## VS Code (optional)

Edit with VS Code on your Mac and run commands in the VM by sharing a folder:

```bash
mkdir -p ~/ailab
multipass mount ~/ailab ailab:/home/ubuntu/ailab
```

Clone into `~/ailab` *inside the VM*, then open `~/ailab` in VS Code on the Mac.
Always run the labs in the VM shell, not the Mac terminal.

## Troubleshooting

| You see | Do this |
|---|---|
| `launch failed: timed out` | Turn off any VPN, then retry. If it still fails: `sudo launchctl kickstart -k system/com.canonical.multipassd` |
| `instance "ailab" already exists` | It's already made. Run `multipass shell ailab`. |
| Can't download the image | Check your network or proxy, or use [Codespaces](codespaces.md). |
| Work Mac blocks VMs | Use [Codespaces](codespaces.md). |

**Already use Docker Desktop or OrbStack?** You can use the repo's dev container
instead of Multipass. See the end of [codespaces.md](codespaces.md).

Guide: https://canonical.com/multipass/docs
