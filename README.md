# Linux for AI-ML Systems

**Every model is a file on a Linux machine. Learn to read the machine.**

A hands-on course by **Emmanuel Naweji** · Transformed 2 Succeed (T2S).
For beginners and working pros who build, train or serve AI models and want to
stop being scared of the server underneath.

📚 **Part of the T2S course library at [transformed2succeed.com/membership](https://www.transformed2succeed.com/membership).**
Subscribe once and get access to **all** T2S courses.

> File at rest. Process at work.
> First question on any broken server: **file problem, or process problem?**

---

## The course

| Module | Title | You'll be able to | Status |
|:-:|---|---|:-:|
| 1 | [The Machine Under Your Model](modules/module-1) | Walk onto a server you've never seen and find 3 problems | ✅ Ready |
| 2 | [Feed the Model](modules/module-2) | Run a disk, permissions and secrets pre-flight before a training job | ✅ Ready |
| 3 | [Keep It Alive](modules/module-3) | Find, watch and stop the processes that serve your model | ✅ Ready |

Each module is ~45 minutes: short sections, one idea each, and a lab that
scores you at the end.

## Before you start: prerequisites

Install these **in this order**. Where each one goes matters.

**On your computer** (Windows / Mac / Chromebook)

1. **A Linux shell.** Pick one (details in [setup/README.md](setup/README.md)):

   | Your computer | Quick start | Full guide |
   |---|---|---|
   | Any (browser only) | This repo → **Code → Codespaces → Create** | [codespaces.md](setup/codespaces.md) |
   | Windows | `wsl --install -d Ubuntu-24.04` | [windows.md](setup/windows.md) |
   | Mac | `brew install --cask multipass` then `multipass launch 24.04 --name ailab` | [mac.md](setup/mac.md) |
   | Linux | Your normal terminal | [linux.md](setup/linux.md) |
   | Chromebook | Settings → Developers → Linux | [chromebook.md](setup/chromebook.md) |

2. **VS Code** (optional): https://code.visualstudio.com. It's the only package that
   goes on your computer. It connects to your Linux shell; each guide shows how.

**Inside your Linux shell**

3. **Git and Python.** Install them in step 1 below.

> ⚠️ Don't install Git or Python on Windows or macOS for this course. Linux
> can't see programs installed there, so you'd still get `command not found`.

## Start in 3 steps

All commands run **inside your Linux shell**.

**1. Install Git and Python** (safe to run even if you already have them)

```bash
sudo apt update && sudo apt install -y git python3
```

Fedora, Arch or another distro? Use the command in [setup/linux.md](setup/linux.md).
Codespaces users can skip this step.

**2. Get the repo and check your machine**

```bash
git clone https://github.com/Here2ServeU/linux-for-ai-ml
cd linux-for-ai-ml && bash setup/doctor.sh
```

Every line should say `OK`.

**3. Start Module 1**

```bash
cd modules/module-1/scripts && python3 make_server.py
cd ~/ai-server && cat README-FIRST.txt
```

## What you need

- A Linux shell (Ubuntu 24.04 is what we test on)
- Git and Python 3.9+ *inside* that Linux shell (step 1 installs them; nothing to install on Windows/macOS)
- VS Code is optional: every lab runs in a plain terminal
- About 1 GB free disk — labs are scaled down on purpose (1 MB here = 1 GB on a real server)
- No GPU needed

## Repo map

```
linux-for-ai-ml/
├── setup/              # doctor.sh + how to get Linux on any computer
├── modules/
│   ├── module-1/       # The Machine Under Your Model (lab + guide)
│   ├── module-2/       # Feed the Model (lab + guide + workbook + slides)
│   └── module-3/       # Keep It Alive (lab + guide)
├── docs/cheatsheet.md  # every command from the course on one page
├── .devcontainer/      # one-click Codespaces setup
└── .github/workflows/  # CI: runs every lab end to end on Ubuntu 24.04
```

## Share your win

Finished Module 1 with **3 / 3**? Post it:

> *The 4-question server checkup: `pwd` · `du -sh * | sort -h` · `grep -rn ERROR logs` · `sha256sum`.
> I ran it on a server I'd never seen and found 3 problems. Try it.*

## Get every course

This repo is one course in the **Transformed 2 Succeed (T2S)** membership.
Subscribe at **[transformed2succeed.com/membership](https://www.transformed2succeed.com/membership)** to get:

- Full access to **all** T2S courses, not just this one
- New modules and courses as they're released

👉 **[Subscribe for access to all courses](https://www.transformed2succeed.com/membership)**

## License

Code: MIT. Course text and slides: © Emmanuel Naweji. See [LICENSE](LICENSE).
