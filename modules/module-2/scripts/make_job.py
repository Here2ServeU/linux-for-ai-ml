#!/usr/bin/env python3
"""
Module 2 lab: build a training job that is about to fail its pre-flight.

    python3 make_job.py            # build ~/ai-job
    python3 make_job.py --reset    # wipe and rebuild it (practice again)
    python3 make_job.py --dir /tmp/ai-job   # build somewhere else
    python3 make_job.py --clean    # delete it when you're done

Sizes are scaled: 1 MB here stands for 1 GB on a real server.
Everything is deterministic, so every student sees the same numbers.

The job hides three pre-flight failures:
  1. Disk        - the scratch space can't fit the run (old temp files)
  2. Permissions - the training data can't be read
  3. Secrets     - an access token is pasted into a config file
"""
import argparse
import os
import random
import shutil
import stat
import sys
from pathlib import Path

KiB = 1024
MiB = 1024 * KiB
SEED = 20261102  # fixed seed -> same bytes for everyone

HERE = Path(__file__).resolve().parent
MARKER = "README-FIRST.txt"

# Obviously fake, but shaped like a real Hugging Face token so grep can find it.
FAKE_TOKEN = "hf_LABfakeTokenNotReal0000000000"


def blob(path: Path, size: int, seed: int) -> None:
    """Write `size` deterministic pseudo-random bytes (fully allocated on disk)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(random.Random(seed).randbytes(size))


def text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.lstrip("\n"))


def jsonl(path: Path, size: int, seed: int) -> None:
    """A fake training dataset: one JSON record per line, about `size` bytes."""
    rng = random.Random(seed)
    words = ("linux model gpu disk file process memory token train serve "
             "loss batch epoch weight layer cuda kernel path log config").split()
    lines, total, i = [], 0, 0
    while total < size:
        sent = " ".join(rng.choice(words) for _ in range(rng.randint(8, 24)))
        line = f'{{"id": {i}, "text": "{sent}"}}\n'
        lines.append(line)
        total += len(line)
        i += 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(lines)[:size])


def build(root: Path) -> None:
    # --- datasets/ ----------------------------------------------------------
    jsonl(root / "datasets/train.jsonl", 6 * MiB, SEED + 1)
    jsonl(root / "datasets/eval.jsonl", 600 * KiB, SEED + 2)

    # --- scratch/ (the job writes checkpoints here while it trains) ----------
    blob(root / "scratch/run-07/step-9500.pt", 1 * MiB, SEED + 10)
    blob(root / "scratch/run-07/step-9600.pt", 1 * MiB, SEED + 11)
    blob(root / "scratch/cache/tokenizer.cache", 512 * KiB, SEED + 12)
    # PROBLEM 1: temp shards from an old run nobody cleaned up.
    for n in range(30):
        blob(root / f"scratch/run-03-tmp/shard-{n:03d}.tmp", 1 * MiB, SEED + 100 + n)

    # --- configs/ -----------------------------------------------------------
    # PROBLEM 3: a token pasted straight into a config file.
    text(root / "configs/train.yaml", f"""
# Fine-tuning job: run-08
base_model: meta-llama/Meta-Llama-3-8B
dataset: datasets/train.jsonl
eval_dataset: datasets/eval.jsonl
scratch_dir: scratch
scratch_quota_mb: 40      # this job may use at most 40 MB of scratch
needs_scratch_mb: 20      # a full run writes about 20 MB of checkpoints
save_every: 100
hf_token: {FAKE_TOKEN}
""")
    text(root / "configs/eval.yaml", """
# Evaluation settings
dataset: datasets/eval.jsonl
batch_size: 16
metrics: [loss, accuracy]
""")

    # Secrets belong in .env, and .env never goes into Git.
    text(root / ".gitignore", """
.env
scratch/
""")

    # --- logs/ --------------------------------------------------------------
    text(root / "logs/run-07.log", """
2026-11-02 01:00:04 INFO  run-07 starting
2026-11-02 01:00:04 INFO  dataset datasets/train.jsonl opened
2026-11-02 01:00:05 INFO  writing checkpoints to scratch/run-07
2026-11-02 06:41:17 INFO  step 9500/9800 (97%) checkpoint saved
2026-11-02 06:44:52 INFO  step 9600/9800 (97%) checkpoint saved
2026-11-02 06:48:30 ERROR No space left on device: scratch/run-07/step-9700.pt
2026-11-02 06:48:30 INFO  run-07 exited with code 1 after 5h48m
""")

    # --- the briefing, the pre-flight and the grader --------------------------
    text(root / MARKER, """
Welcome to ai-job. Last night's run died at 97% after almost 6 hours.
Run-08 is next, and it will fail too. Find out why before you press start.

Three pre-flight checks fail. Find them before you change anything.

  Mission 1 - Disk:        Will it fit? What is filling the scratch space?  (which folder?)
  Mission 2 - Permissions: Which file can the job not read?                 (path to the file)
  Mission 3 - Secrets:     Which file has a secret pasted into it?          (path to the file)

Check the job:     bash preflight.sh        (says GO or NO-GO)
Score yourself:    bash check_answers.sh <folder> <unreadable-file> <file-with-secret>

Sizes are scaled: 1 MB here stands for 1 GB on a real server.
The token in this job is fake. Never paste a real one anywhere in a lab.
""")
    for name in ("check_answers.sh", "preflight.sh"):
        shutil.copyfile(HERE / name, root / name)

    # PROBLEM 2: write-only for the owner (--w-------). Set last so the build can write it.
    (root / "datasets/train.jsonl").chmod(0o200)


def remove(root: Path) -> None:
    """rmtree that also handles folders a student chmod'ed shut (e.g. chmod 000)."""
    os.chmod(root, stat.S_IRWXU)
    # Top-down walk: unlock each sub-folder before os.walk tries to list it.
    for d, dirs, _ in os.walk(root):
        for name in dirs:
            p = os.path.join(d, name)
            if not os.path.islink(p):
                os.chmod(p, stat.S_IRWXU)
    shutil.rmtree(root)


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the Module 2 practice training job.")
    ap.add_argument("--dir", default=str(Path.home() / "ai-job"),
                    help="where to build it (default: ~/ai-job)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--reset", action="store_true",
                      help="delete the existing job and rebuild it")
    mode.add_argument("--clean", action="store_true",
                      help="delete the job and stop (clean up when you're done)")
    args = ap.parse_args()
    root = Path(args.dir).expanduser().resolve()

    if args.clean:
        if not root.exists():
            print(f"Nothing to clean: {root} doesn't exist.")
            return 0
        if not (root / MARKER).exists():
            print(f"Refusing to delete {root}: it doesn't look like a lab job.")
            return 1
        remove(root)
        print(f"Removed {root}. Disk reclaimed.")
        print("Exported HF_TOKEN for the lab? Clear it too:  unset HF_TOKEN")
        return 0

    if root.exists():
        if not args.reset:
            print(f"{root} already exists. Use --reset to rebuild it.")
            return 1
        if not (root / MARKER).exists():
            print(f"Refusing to delete {root}: it doesn't look like a lab job.")
            return 1
        remove(root)

    build(root)
    print(f"Built your training job at {root}")
    print(f"Next:  cd {root} && cat README-FIRST.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
