# Pick your Linux. Any one works.

Ten minutes, once. Every command in this course then runs the same way.

| Your computer | Use | Guide |
|---|---|---|
| Anything with a browser (school/work laptop, iPad, no admin rights) | GitHub Codespaces | [codespaces.md](codespaces.md) |
| Windows 10 / 11 | WSL (Ubuntu inside Windows) | [windows.md](windows.md) |
| Mac (Apple Silicon or Intel) | Multipass (small Ubuntu VM) | [mac.md](mac.md) |
| Already on Linux (Ubuntu, Debian, Fedora, Arch, …) | Your own terminal | [linux.md](linux.md) |
| Chromebook | Built-in Linux development environment | [chromebook.md](chromebook.md) |

Done when this prints `All 5 checks OK`:

```bash
bash setup/doctor.sh
```

## What you do *not* need to install first

- **Python and Git**: don't install them on Windows or macOS. You need them
  *inside Linux*, and Ubuntu 24.04 (Codespaces, WSL, Multipass) already has them.
  If one is missing, the doctor prints the one command that adds it.
- **VS Code**: optional. All labs run in a plain terminal. If you like VS Code,
  each guide shows how to point it at your Linux shell.
- **A GPU**: not needed for Modules 1-3.

## Why not just use the Mac terminal or Git Bash?

They look like Linux but aren't. macOS uses BSD tools (`sed -i` needs different
arguments, and `du` and `find` flags differ, with no `/proc`). Git Bash on
Windows is a thin layer over Windows. The servers your models run on are Linux,
so the course is too. That's why the doctor fails on them.

---

**Stuck for 15 minutes?** Switch to [Codespaces](codespaces.md). It runs in your
browser, and the course works the same there.

---

📚 Part of **Linux for AI-ML Systems**, a T2S course. Subscribe at
**[transformed2succeed.com/membership](https://www.transformed2succeed.com/membership)** for access to all courses.
