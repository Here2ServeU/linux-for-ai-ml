# Module 1 · The Machine Under Your Model

**Core idea:** a model is just a big file on a Linux computer. Learn to find it
and read it, and you can fix it.

**Memory hook:** File at rest. Process at work.

~45 min · 6 sections · 1 lab

| # | Section | Time | The one idea |
|:-:|---|:-:|---|
| 01 | Where Does a Model Live? | ~6 min | 8B params × 2 bytes ≈ 16 GB: a model is a file you can measure. |
| 02 | The House Map | ~8 min | One tree from `/`. Every room has one job. Absolute vs relative paths. |
| 03 | Talk to the Machine | ~8 min | A command is a sentence: program, flags, argument. Nine moves. |
| 04 | Find, Inspect, Measure | ~7 min | Measure before you move: `find`, `du`/`df`, `head`/`grep`/`file`. |
| 05 | Pipes: Small Tools, Big Answers | ~6 min | `du -ah \| sort -rh \| head -3`: one question, one answer. |
| 06 | Build It: Map a Server You've Never Seen | ~10 min | Find the disk hog, the path typo and the duplicate model. |

---

## The lab: map a server you've never seen

### Step 1 · Get the lab, check your machine

Run this inside your Linux shell (no Linux yet? [setup/README.md](../../setup/README.md)):

```bash
sudo apt update && sudo apt install -y git python3   # other distros: setup/linux.md
git clone https://github.com/Here2ServeU/linux-for-ai-ml
cd linux-for-ai-ml && bash setup/doctor.sh
```

Codespaces users: Git and Python are installed and the repo is already cloned. Just run the doctor.

### Step 2 · Build the server

```bash
cd modules/module-1/scripts && python3 make_server.py
cd ~/ai-server && cat README-FIRST.txt
```

This builds a small, realistic model server in your home folder: models,
checkpoints, a dataset, configs and logs. Your three missions:

1. **Disk** — What is eating the disk?
2. **Startup** — Why won't the LLM server start?
3. **Duplicate** — Which model file is wasted space?

Try them yourself first. The walkthrough is below.

<details>
<summary><b>Step 3 · Mission 1: what's eating the disk?</b></summary>

```bash
du -sh * | sort -h
du -ah models | sort -rh | head -5
```

You should see (biggest last):

```
8.0K  logs
12K   configs
8.9M  datasets
25M   checkpoints
39M   models
```

Then `39M models`, with `17M models/old/llama-3-8b-backup` near the top —
the same size as the real model. Suspicious.
</details>

<details>
<summary><b>Step 4 · Mission 2: why won't the LLM server start?</b></summary>

```bash
grep -rn ERROR logs
ls models
grep -n model_path configs/*.yaml
```

```
logs/server.log:6: ... ERROR model file not found: models/llama3-8b/model.safetensors
embed-mini  llama-3-8b  old
configs/serve.yaml:3:model_path: models/llama3-8b/model.safetensors
```

One missing dash: `llama3-8b` vs `llama-3-8b`. File problem, not a process problem.
</details>

<details>
<summary><b>Step 5 · Mission 3: which file is a wasted duplicate?</b></summary>

```bash
find models -name '*.safetensors' -exec sha256sum {} +
```

Two lines share the fingerprint `4c7ff86c…`. Same fingerprint = same bytes.
On a real server, that's 16 GB of disk doing nothing.
</details>

<details>
<summary><b>Step 6 · Fix it, then check your answers</b></summary>

```bash
sed -i 's/llama3-8b/llama-3-8b/' configs/serve.yaml
rm -r models/old
bash check_answers.sh models configs/serve.yaml models/old/llama-3-8b-backup/model.safetensors
```

```
Score: 3 / 3
You just diagnosed a server you had never seen.
```

⚠️ `rm` has no undo and no trash can. Only delete after you've **proved** it's a
copy, like you just did with `sha256sum`. Measure, prove, then delete.
</details>

### Practice again

```bash
cd ~/linux-for-ai-ml/modules/module-1/scripts && python3 make_server.py --reset
```

Goal: solve all three in under 5 minutes.

---

## Exercises (before Module 2)

1. **Run the doctor** — `bash setup/doctor.sh` until every line says OK.
2. **Tour the house** — `ls` each of `/ /etc /var/log /dev`. One job per room.
3. **Translate 3 commands** — write `ls -lh`, `du -sh`, `grep -rn` as English.
4. **Absolute vs relative** — `cd /tmp`, then reach `~/ai-server` both ways.
5. **Biggest 3 files** — `du -ah ~ | sort -rh | head -3`
6. **Find by size** — `find ~ -size +5M` lists files over 5 MB.
7. **Break & fix** — `make_server.py --reset`, then solve all 3 again in 5 min.
8. **Teach it** — explain "file at rest, process at work" to a friend.

**Practice task (2 min):** run `du -sh ~/* | sort -h` on any Linux machine. Name the
biggest thing in your home folder and decide whether it's a file problem waiting to happen.

**Self-check (from memory):** *A model server won't start. What's your very first question?*

<details><summary>Answer</summary>

File problem or process problem? Then `grep` the logs for `ERROR` and `ls` what really exists.
</details>

**Next:** Module 2 reuses `du` from this lab in its pre-flight check.

---

📚 Part of **Linux for AI-ML Systems**, a T2S course. Subscribe at
**[transformed2succeed.com/membership](https://www.transformed2succeed.com/membership)** for access to all courses.
