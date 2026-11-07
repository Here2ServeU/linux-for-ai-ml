# Any computer · GitHub Codespaces

The easiest option. Linux runs in GitHub's cloud and you use it in your browser.
Nothing to install, and it works on locked-down work or school laptops.

**You need:** a free GitHub account (https://github.com/signup).

## Steps

1. Open https://github.com/Here2ServeU/linux-for-ai-ml
2. Click **Code → Codespaces → Create codespace on main**
3. Wait 1-2 minutes. The doctor runs on its own the first time.
4. To run it again, in the terminal at the bottom:

   ```bash
   bash setup/doctor.sh
   ```

The repo is already cloned, and Python and Git are already installed.

## Good to know

- **Free hours:** personal accounts get a monthly free quota, which is far more
  than this course needs. Stop the codespace when you're done:
  https://github.com/codespaces → **⋯ → Stop codespace**.
- **Coming back:** reopen it from https://github.com/codespaces. Your files are
  kept until you delete the codespace.
- **No terminal visible?** Menu **☰ → Terminal → New Terminal**.
- **Prefer desktop VS Code?** In the codespace, click **☰ → Open in VS Code Desktop**.

## Same container on your own machine (optional)

If you have Docker Desktop (or OrbStack on Mac) and VS Code with the
**Dev Containers** extension: clone the repo, open the folder in VS Code, then
**Command Palette → Dev Containers: Reopen in Container**. You get the same
Ubuntu 24.04 environment as Codespaces, defined in `.devcontainer/devcontainer.json`.

Guide: https://docs.github.com/codespaces
