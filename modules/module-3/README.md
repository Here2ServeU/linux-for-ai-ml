# Module 3 · Keep It Alive

**Core idea:** the right-hand box from Module 1 — *process at work*. A running
model is a process with a PID. Learn to find it, watch it and stop it safely.

**Memory hook:** Find it, watch it, stop it: polite first.

~45 min · 5 sections · 1 lab

| # | Section | Time | The one idea |
|:-:|---|:-:|---|
| 01 | Meet the Process | ~8 min | `ps`, PIDs and `/proc`: a model server is just a program running. |
| 02 | Watch It Work | ~8 min | `top`/`htop`, `free -h`, `nvidia-smi`: CPU, memory, GPU. |
| 03 | Stop It Safely | ~8 min | `kill`, signals, Ctrl-C vs `kill -9`. |
| 04 | Keep It Running | ~9 min | `systemd` services, `journalctl` logs, restart on failure. |
| 05 | Build It: Rescue a Slow Server | ~12 min | Find the runaway process, free the memory, keep the model server up. |

---

## The lab: rescue a slow server

The lab uses ordinary processes that you own. It needs no root and no
`systemd`, so it runs the same in Codespaces, WSL, Multipass and plain Linux
(Codespaces and some WSL setups have no `systemd` at all). Section 04's
`systemctl` commands are for real servers. Try them in Multipass or on your own Linux box.

### Step 1 · Get the lab

```bash
cd ~/linux-for-ai-ml && git pull && bash setup/doctor.sh
```

New here? Follow Step 1 in [Module 1](../module-1/README.md#step-1--get-the-lab-check-your-machine) first.

### Step 2 · Start the server

```bash
cd ~/linux-for-ai-ml/modules/module-3/scripts && python3 make_lab.py
cd ~/ai-lab && cat README-FIRST.txt
```

This starts three programs in the background. One is `llm-serve`, the model
server, and users say it's slow. Your three missions:

1. **CPU** — Which program is burning a full CPU core?
2. **Memory** — Which program is holding the most memory?
3. **Server** — What is the PID of the model server, `llm-serve`?

Then stop the two bad programs and keep `llm-serve` running.
Try it yourself first. The walkthrough is below.

<details>
<summary><b>Step 3 · Mission 1: what's burning the CPU?</b></summary>

```bash
ps aux --sort=-%cpu | head -5
```

```
USER   PID   %CPU %MEM    RSS ... COMMAND
you    4242  99.0  1.0  10212 ... /usr/bin/python3 /home/you/ai-lab/bin/data-loader
you    4243   2.6 16.8 163808 ... /usr/bin/python3 /home/you/ai-lab/bin/cache-warmer
you    4241   0.3  1.0  10216 ... /usr/bin/python3 /home/you/ai-lab/bin/llm-serve
```

Or run `top` (press `P` to sort by CPU, `q` to quit). `data-loader` is at ~100%:
one full core. Why? Ask its log:

```bash
tail logs/data-loader.log     # "retrying forever (no backoff)"
```

Your PIDs will differ from these. That's normal: the kernel hands them out.
</details>

<details>
<summary><b>Step 4 · Mission 2: what's holding the memory?</b></summary>

```bash
free -h
ps aux --sort=-%mem | head -5
```

`cache-warmer` holds about 160 MB (the `RSS` column, in KB), far more than
the others. In `top`, press `M` to sort by memory.
</details>

<details>
<summary><b>Step 5 · Mission 3: find the model server</b></summary>

```bash
pgrep llm-serve
ls /proc/$(pgrep llm-serve)        # a process is a folder in /proc
tail -3 logs/llm-serve.log         # "healthy: 42 requests served"
```

That PID is the one process you must **not** stop.
</details>

<details>
<summary><b>Step 6 · Stop it safely, then check your answers</b></summary>

Polite first. `kill` sends SIGTERM: "please finish up and exit".

```bash
kill $(pgrep data-loader)
kill $(pgrep cache-warmer)
pgrep -l data-loader            # nothing: it exited cleanly
pgrep -l cache-warmer           # still there!
tail -2 logs/cache-warmer.log   # "got SIGTERM, ignoring it"
```

`cache-warmer` ignores SIGTERM. Only now escalate to SIGKILL, which a program
can't ignore (and which gives it no chance to clean up):

```bash
kill -9 $(pgrep cache-warmer)
free -h                          # the memory is back
```

```bash
bash check_answers.sh data-loader cache-warmer $(pgrep llm-serve)
```

```
Score: 3 / 3
  Fix check: data-loader stopped. CPU is free.
  Fix check: cache-warmer stopped. Memory is back.
  Fix check: llm-serve is still running. Users are being served.
You just rescued a server without taking the model down.
```

⚠️ `kill -9` is the last step, not the first. Try `kill`, wait a few seconds,
read the log, *then* escalate. And always check the PID before you press Enter.
</details>

### Section 04 · Keep it running (on a server with systemd)

On a real server, `llm-serve` would be a `systemd` service that comes back by itself:

```bash
systemctl status llm-serve          # running? since when? last log lines
sudo systemctl restart llm-serve    # stop + start
journalctl -u llm-serve -n 50       # its last 50 log lines
journalctl -u llm-serve -f          # follow live (Ctrl-C to stop)
```

With `Restart=on-failure` in its unit file, systemd starts it again if it crashes.
That's why, on a real server, you stop a service with `systemctl stop`, not
`kill`: otherwise systemd may just start it again.

### Practice again

```bash
cd ~/linux-for-ai-ml/modules/module-3/scripts && python3 make_lab.py --reset
```

Goal: all three missions, model server still up, in under 5 minutes.

### Clean up

Done with the lab? Stop every lab process and remove the folder:

```bash
cd ~/linux-for-ai-ml/modules/module-3/scripts && python3 make_lab.py --clean
pgrep -l 'llm-serve|data-loader|cache-warmer' || echo "all stopped"
```

It only stops processes the lab started and only deletes a folder the lab built.
Forgot to clean up? Every lab process exits on its own after 2 hours anyway.
Built it somewhere else with `--dir`? Pass the same `--dir` to `--clean`.

---

## Exercises

1. **Your own processes** — `ps -u $USER | wc -l`. How many are you running right now?
2. **Who's PID 1?** — `ps -p 1 -o pid,comm`. Every other process descends from it.
3. **Read /proc** — `cat /proc/$$/status | head -5` (`$$` is your shell's own PID).
4. **Ctrl-C is a signal** — run `sleep 100`, press Ctrl-C. That sent SIGINT.
5. **Background a job** — `sleep 300 &`, then `jobs`, `pgrep -l sleep`, `kill %1`.
6. **Watch it live** — open `top`, press `M`, then `P`. What's using your machine?
7. **Break & fix** — `make_lab.py --reset`, then rescue it again in 5 min.

**Self-check (from memory):** *A model server is slow. What do you do, in order?*

<details><summary>Answer</summary>

Find the busy process (`ps aux --sort=-%cpu`, `top`), check memory (`free -h`, `--sort=-%mem`),
read its log, then `kill` politely. Use `kill -9` only if it ignores you, and never stop the model server by mistake.
</details>

**You've finished the course.** File at rest, process at work: you can now read both.

---

📚 Part of **Linux for AI-ML Systems**, a T2S course. Subscribe at
**[transformed2succeed.com/membership](https://www.transformed2succeed.com/membership)** for access to all courses.
