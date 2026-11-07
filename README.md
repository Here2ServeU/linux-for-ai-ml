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
| 2 | [Feed the Model](modules/module-2) | Run a disk, permissions and secrets pre-flight before a training job | 🛠 Coming |
| 3 | [Keep It Alive](modules/module-3) | Find, watch and stop the processes that serve your model | 🛠 Coming |

Each module is ~45 minutes: short sections, one idea each, and a lab that
scores you at the end.

## Start in 3 steps

**1. Get a Linux shell** (pick one — details in [setup/README.md](setup/README.md))

| Any computer | Windows | Mac |
|---|---|---|
| This repo → **Code → Codespaces → Create** | `wsl --install -d Ubuntu-24.04` | `brew install --cask multipass` then `multipass launch 24.04 --name ailab` |

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
- Git and Python 3.9+ (already on Codespaces and Ubuntu 24.04)
- About 1 GB free disk — labs are scaled down on purpose (1 MB here = 1 GB on a real server)
- No GPU needed

## Repo map

```
linux-for-ai-ml/
├── setup/              # doctor.sh + how to get Linux on any computer
├── modules/
│   ├── module-1/       # The Machine Under Your Model (lab + guide)
│   ├── module-2/       # Feed the Model
│   └── module-3/       # Keep It Alive
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
