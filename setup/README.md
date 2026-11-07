# Pick your Linux. Any one works.

Ten minutes, once. Every command in this course then runs the same way.

## Any computer · GitHub Codespaces (easiest)

1. Open this repo on github.com
2. **Code → Codespaces → Create codespace on main**
3. In the terminal: `bash setup/doctor.sh`

Guide: https://docs.github.com/codespaces

## Windows · WSL

In **PowerShell (Admin)**:

```powershell
wsl --install -d Ubuntu-24.04
```

Restart, open **Ubuntu** from the Start menu, then:

```bash
sudo apt update && sudo apt install -y git python3
git clone https://github.com/Here2ServeU/linux-for-ai-ml
cd linux-for-ai-ml && bash setup/doctor.sh
```

Guides: https://learn.microsoft.com/windows/wsl/install · https://documentation.ubuntu.com/wsl

## Mac · Multipass

Install Homebrew first (https://brew.sh), then in **Terminal**:

```bash
brew install --cask multipass
multipass launch 24.04 --name ailab
multipass shell ailab
```

Inside the VM:

```bash
sudo apt update && sudo apt install -y git python3
git clone https://github.com/Here2ServeU/linux-for-ai-ml
cd linux-for-ai-ml && bash setup/doctor.sh
```

Guide: https://canonical.com/multipass/install

---

**Stuck for 15 minutes?** Switch to Codespaces. It runs in your browser, and the
course works the same there.

---

📚 Part of **Linux for AI-ML Systems**, a T2S course. Subscribe at
**[transformed2succeed.com/membership](https://www.transformed2succeed.com/membership)** for access to all courses.
