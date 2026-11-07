# Chromebook · Linux development environment

Most Chromebooks from 2019 or later can run Debian Linux built in.

## Steps

1. **Settings → About ChromeOS → Developers → Linux development environment → Set up**
   (on older versions: **Settings → Advanced → Developers**)
2. Accept the defaults (a 10 GB disk is plenty). A **Terminal** window opens.
3. In the Terminal:

   ```bash
   sudo apt update && sudo apt install -y git python3
   git clone https://github.com/Here2ServeU/linux-for-ai-ml
   cd linux-for-ai-ml && bash setup/doctor.sh
   ```

Later, open **Terminal** from the app launcher and pick **penguin**.

## Troubleshooting

- **No "Developers" or "Linux" option:** your school or work admin has turned it
  off, or the Chromebook is too old. Use [Codespaces](codespaces.md).
- **Python is older than 3.9:** update ChromeOS, then in Terminal run
  `sudo apt update && sudo apt full-upgrade -y`. Or use Codespaces.

Guide: https://support.google.com/chromebook/answer/9145439
