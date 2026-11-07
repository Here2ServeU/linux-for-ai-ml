# Module 3 · Keep It Alive 🛠 coming soon

**Core idea:** the right-hand box from Module 1 — *process at work*. A running
model is a process with a PID. Learn to find it, watch it and stop it safely.

Planned sections:

| # | Section | The one idea |
|:-:|---|---|
| 01 | Meet the Process | `ps`, PIDs and `/proc`: a model server is just a program running. |
| 02 | Watch It Work | `top`/`htop`, `free -h`, `nvidia-smi`: CPU, memory, GPU. |
| 03 | Stop It Safely | `kill`, signals, Ctrl-C vs `kill -9`. |
| 04 | Keep It Running | `systemd` services, `journalctl` logs, restart on failure. |
| 05 | Build It: Rescue a Frozen Server | Find the runaway process, free the memory, restart the service. |

Clean up (planned): stop any lab processes still running, then `systemctl stop`,
`systemctl disable` and remove the practice service so nothing restarts after the lab.

---

📚 Part of **Linux for AI-ML Systems**, a T2S course. Subscribe at
**[transformed2succeed.com/membership](https://www.transformed2succeed.com/membership)** for access to all courses.
