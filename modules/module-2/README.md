# Module 2 · Feed the Model 🛠 coming soon

**Core idea:** most training jobs that die at 97% died before they started.
Disk, permissions and secrets: a three-part pre-flight check stops that.

Planned sections:

| # | Section | The one idea |
|:-:|---|---|
| 01 | Will It Fit? | `df -h` + `du -sh` before every download or training run (reuses Module 1). |
| 02 | Who Can Read It? | Owners, groups and `rwx`: `ls -l`, `chmod`, `chown`. |
| 03 | Keep Secrets Secret | API keys and tokens: environment variables, `.env`, `chmod 600`, never in Git. |
| 04 | Build It: The Pre-Flight Script | One script that says GO / NO-GO before a job starts. |

Lab (planned): `scripts/make_job.py` builds a training job with three hidden
pre-flight failures; `check_answers.sh` scores your fixes.

---

📚 Part of **Linux for AI-ML Systems**, a T2S course. Subscribe at
**[transformed2succeed.com/membership](https://www.transformed2succeed.com/membership)** for access to all courses.
