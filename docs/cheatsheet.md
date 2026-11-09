# Cheat sheet · Linux for AI-ML Systems

## The 4-question server checkup

| # | Question | Command |
|:-:|---|---|
| 1 | Where am I? | `pwd` · `ls -lh` |
| 2 | What's big? | `du -sh * \| sort -h` |
| 3 | What's wrong? | `grep -rn ERROR logs` |
| 4 | What's doubled? | `sha256sum file` |

## Nine moves cover most days

| Command | What it does |
|---|---|
| `pwd` | Where am I? |
| `ls -lh` | What's here? Long list, human sizes |
| `cd folder` · `cd ..` · `cd ~` | Walk in · step back · go home |
| `cat file` · `less file` | Read a file (`q` quits less) |
| `head` · `tail` · `tail -f` | First/last 10 lines · follow a live log |
| `Tab` | Auto-complete names |
| `↑` · `history` | Re-run what you typed before |
| `Ctrl-C` | Stop whatever is running |
| `man cmd` · `cmd --help` | The built-in manual |

## Find, inspect, measure

| Command | What it does |
|---|---|
| `find ~ -name '*.safetensors'` | Find files by name |
| `find ~ -size +5M` | Find files over 5 MB |
| `du -sh *` | Size of each thing here |
| `du -ah dir \| sort -rh \| head -5` | 5 biggest things in dir |
| `df -h` | Free space on each disk |
| `grep -rn WORD dir` | Every line with WORD, with file + line number |
| `file thing` | What type of file is this? |
| `sha256sum file` | Fingerprint: same bytes, same string |
| `sed -i 's/old/new/' file` | Search and replace inside a file |
| `rm -r dir` | Delete a folder. **No undo.** |

## Symbols

| Symbol | Meaning |
|---|---|
| `$` | The prompt. Never type it. |
| `# note` | A comment, ignored |
| `-lh` | Stacked flags (`-l -h`) |
| `~` | Your home folder |
| `*` | Wildcard: any name |
| `A \| B` | Pipe: A's output into B |
| `A && B` | Run B only if A worked |
| `'quotes'` | Keep a pattern in one piece |
| `2>/dev/null` | Hide error messages |

## The house map

`/` front door · `/home` your desk · `/opt` workshop · `/etc` rule book ·
`/var/log` diary · `/tmp` scratch paper · `/dev` devices (GPUs: `/dev/nvidia0`) ·
`/proc` live feed

## Pre-flight: disk, permissions, secrets (Module 2)

| Command | What it does |
|---|---|
| `df -h .` | Free space on the disk you're standing on |
| `du -sh dir/* \| sort -h` | What's filling this folder |
| `ls -l` | Owner, group and `rwx` bits for each file |
| `chmod 644 file` | Owner reads + writes, everyone else reads |
| `chmod 600 .env` | Only you can read or write it (secrets) |
| `sudo chown you:you file` | Make yourself the owner |
| `grep -rn token configs` | Hunt for pasted secrets |
| `export NAME=value` · `unset NAME` | Set / clear an environment variable |

`rwx` = read 4 · write 2 · execute 1. Owner, group, others: `rw-r--r--` = 644.

## Processes (Module 3)

| Command | What it does |
|---|---|
| `ps aux --sort=-%cpu \| head -5` | Top CPU users |
| `ps aux --sort=-%mem \| head -5` | Top memory users |
| `top` (`P` CPU · `M` memory · `q` quit) | Live view |
| `free -h` | Memory in use and free |
| `pgrep name` · `pgrep -l name` | PID(s) of a program |
| `ls /proc/PID` | A process is a folder in `/proc` |
| `kill PID` | Polite stop (SIGTERM). Always try first |
| `kill -9 PID` | Forced stop (SIGKILL). Last resort |
| `systemctl status svc` · `journalctl -u svc -f` | A service and its live logs |
