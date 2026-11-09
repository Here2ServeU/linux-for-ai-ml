#!/usr/bin/env python3
"""
Module 3 lab: start a model server that is in trouble.

    python3 make_lab.py            # build ~/ai-lab and start its processes
    python3 make_lab.py --reset    # stop everything, rebuild, start again
    python3 make_lab.py --dir /tmp/ai-lab   # build somewhere else
    python3 make_lab.py --clean    # stop every lab process and delete the folder

No root and no systemd needed: these are ordinary processes owned by you,
so the lab runs the same in Codespaces, WSL, Multipass and plain Linux.

Three programs start in the background:
  llm-serve     - the model server. Healthy. It must stay running.
  data-loader   - PROBLEM 1: stuck in a loop, burning a full CPU core.
  cache-warmer  - PROBLEM 2: holds ~150 MB of memory and ignores a plain `kill`.

Safety net: every lab process exits on its own after 2 hours.
"""
import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
MARKER = "README-FIRST.txt"
STATE = ".lab-state"
NAMES = ("llm-serve", "data-loader", "cache-warmer")

# One small program; each copy behaves according to its name.
PROGRAM = r'''#!/usr/bin/env python3
# Module 3 lab process. Safe to stop. Exits by itself after 2 hours.
import ctypes, os, signal, sys, time

NAME = os.path.basename(sys.argv[0])
LIFETIME = 2 * 60 * 60
start = time.time()

# Show up as NAME (not python3) in top, ps -e and pgrep.
try:
    ctypes.CDLL(None).prctl(15, NAME.encode(), 0, 0, 0)  # PR_SET_NAME
except Exception:
    pass

def log(msg):
    print(time.strftime("%Y-%m-%d %H:%M:%S"), NAME, f"[pid {os.getpid()}]", msg, flush=True)

def stop_cleanly(signum, frame):
    log(f"got {signal.Signals(signum).name}, shutting down cleanly")
    sys.exit(0)

def ignore(signum, frame):
    log(f"got {signal.Signals(signum).name}, ignoring it: still flushing the cache")

if NAME == "llm-serve":
    signal.signal(signal.SIGTERM, stop_cleanly)
    log("listening on port 8000, model models/llama-3-8b loaded")
    served = 0
    while time.time() - start < LIFETIME:
        time.sleep(5)
        served += 7
        log(f"healthy: {served} requests served")

elif NAME == "data-loader":
    signal.signal(signal.SIGTERM, stop_cleanly)
    log("preprocessing shard 0")
    log("WARN shard 0 failed, retrying forever (no backoff)")
    n = 0
    while True:                      # a busy loop: one full CPU core
        n += 1
        if n % 5_000_000 == 0 and time.time() - start > LIFETIME:
            break

elif NAME == "cache-warmer":
    signal.signal(signal.SIGTERM, ignore)
    log("warming cache")
    cache = bytearray(150 * 1024 * 1024)
    for i in range(0, len(cache), 4096):   # touch every page so it's really in RAM
        cache[i] = 1
    log("holding 150 MB of cache, never released")
    while time.time() - start < LIFETIME:
        time.sleep(5)

log("lab time limit reached, exiting")
'''


def pid_matches(pid: int, root: Path, name: str) -> bool:
    """True only if `pid` is still our lab program (PIDs get reused)."""
    try:
        cmd = Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")
    except OSError:
        return False
    return str(root / "bin" / name).encode() in cmd


def lab_pids(root: Path) -> dict:
    """Every running lab process under root, found by command line."""
    found = {}
    for d in Path("/proc").iterdir():
        if d.name.isdigit():
            for name in NAMES:
                if pid_matches(int(d.name), root, name):
                    found[int(d.name)] = name
    return found


def stop_all(root: Path) -> int:
    pids = lab_pids(root)
    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    deadline = time.time() + 3
    while time.time() < deadline and lab_pids(root):
        time.sleep(0.2)
    for pid, name in lab_pids(root).items():      # cache-warmer ignores SIGTERM
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    return len(pids)


def build_and_start(root: Path) -> None:
    (root / "bin").mkdir(parents=True)
    (root / "logs").mkdir()
    for name in NAMES:
        p = root / "bin" / name
        p.write_text(PROGRAM)
        p.chmod(0o755)

    (root / MARKER).write_text("""\
Welcome to ai-lab. Users say the model server is slow, and the machine's fan
is screaming. Three programs are running here. One of them is the model server.

Find the problems before you stop anything.

  Mission 1 - CPU:     Which program is burning a full CPU core?        (its name)
  Mission 2 - Memory:  Which program is holding the most memory?        (its name)
  Mission 3 - Server:  What is the PID of the model server, llm-serve?  (a number)

Then fix it: stop the two bad programs, and keep llm-serve running.
Hint: try a polite kill first. If a program ignores it, escalate.

Logs are in logs/. Score yourself:
  bash check_answers.sh <cpu-program> <memory-program> <llm-serve-pid>

Every lab process stops by itself after 2 hours.
Done? Stop everything:  python3 make_lab.py --clean   (from the scripts folder)
""")
    (root / "check_answers.sh").write_bytes((HERE / "check_answers.sh").read_bytes())

    state = []
    for name in NAMES:
        log = open(root / "logs" / f"{name}.log", "ab")
        proc = subprocess.Popen(
            [sys.executable, str(root / "bin" / name)],
            cwd=root, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
            start_new_session=True,  # keeps running after this script and your shell exit
        )
        state.append(f"{name}={proc.pid}")
    (root / STATE).write_text("\n".join(state) + "\n")
    time.sleep(1)  # let them start (and let the cache fill) before you look


def main() -> int:
    ap = argparse.ArgumentParser(description="Start the Module 3 practice server.")
    ap.add_argument("--dir", default=str(Path.home() / "ai-lab"),
                    help="where to build it (default: ~/ai-lab)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--reset", action="store_true",
                      help="stop everything, rebuild and start again")
    mode.add_argument("--clean", action="store_true",
                      help="stop every lab process and delete the folder")
    args = ap.parse_args()
    root = Path(args.dir).expanduser().resolve()

    if not Path("/proc/self/cmdline").exists():
        print("This lab needs Linux (it reads /proc). Run it inside your Linux shell.")
        return 1

    if args.clean:
        if not root.exists():
            print(f"Nothing to clean: {root} doesn't exist.")
            return 0
        if not (root / MARKER).exists():
            print(f"Refusing to delete {root}: it doesn't look like a lab folder.")
            return 1
        n = stop_all(root)
        subprocess.run(["rm", "-rf", "--", str(root)], check=True)
        print(f"Stopped {n} lab process(es) and removed {root}.")
        return 0

    if root.exists():
        if not args.reset:
            print(f"{root} already exists. Use --reset to start over.")
            return 1
        if not (root / MARKER).exists():
            print(f"Refusing to delete {root}: it doesn't look like a lab folder.")
            return 1
        stop_all(root)
        subprocess.run(["rm", "-rf", "--", str(root)], check=True)

    build_and_start(root)
    print(f"Started 3 programs in the background. Your lab is at {root}")
    print(f"Next:  cd {root} && cat README-FIRST.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
