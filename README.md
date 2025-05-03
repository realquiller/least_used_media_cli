# 🎯 Least Used Media Finder (CLI)

A cross-platform Python command-line tool that helps video editors discover neglected media files (e.g. `.mp3`, `.mp4`, `.wav`) in their storage directories.

Originally created to improve my own DaVinci Resolve workflow, this project helps surface hidden gems that haven’t been touched in months — or even years.

> 🤖 Built in Python 3, tested on Windows & Git Bash, compatible with Linux/macOS.

## ✨ Features

## ✨ Features

- `-l`, `--limit` — Show only the first N results
- `-f`, `--folder` — Specify a subfolder inside your media folder
- `-r`, `--random` — Shuffle results to increase variety
- `-n`, `--newest` — Only show files unused for at least X days
- `-i`, `--ignore-recent` — Ignore files accessed in the last X days
- `-e`, `--extension` — Filter by one or more extensions (`.mp3`, `.wav`, `.mp4`, etc.)
- `-p`, `--play` — Open files with your system’s default player
- `--log-to` — Save output to a `.txt` log file in a path starting from the root of the project folder

## 💡 Example Usage

```bash
python least_used.py --limit 10 --random --extension .mp3 .wav --ignore-recent 2 --play
```
```bash
python least_used.py --folder memes --newest 90 --log-to logs/meme_archive.txt
```
```bash
python least_used.py --extension .mp4 --limit 5 --play
```

## ⚙️ Setup

1. Clone this repo:
   ```bash
   git clone https://github.com/realquiller/least_used_media_cli.git
   cd least-used-media-cli
   ```
2. Create a file named least_used_config.txt in the same folder as the script.
   Inside it, paste the full path to your media folder (e.g., C:\Stream or /home/yourname/media).

3. Run the app:
   ```bash
   python least_used.py
   ```
4. Optional:
   Install ffplay, VLC, or ensure your system has a default player for --play to work.

## 🧠 Why I Built This

As a YouTuber and video editor, I was hoarding hundreds of sound effects and meme clips — but forgetting about most of them. This tool helps me uncover older, forgotten media files that might spice up my content.

It’s now a core part of my workflow when I'm selecting audio/visual elements for my videos. The `--random` and `--play` features in particular help spark creative ideas from old files I haven't touched in a while.

## 📚 What I Learned

- Building real command-line tools using `argparse`
- Handling file system traversal with `os.walk`
- Managing timestamps (`os.stat().st_atime`)
- File filtering, truncation, and sorting
- Designing an intuitive CLI experience
- Logging, clipboard, and (attempted) cross-platform clipboard support
- Using system default players with `subprocess` (`--play`)
- Planning future `.exe` GUI versions

This project helped me break free from perfectionist tutorials and actually build something practical, personal, and technical.

## 🔮 Future Features

- GUI version using Tkinter or Electron
- Save presets (e.g., favorite folder/extension combos)
- Drag-and-drop launcher for `.exe` users
- Better audio waveform preview
- Smart scoring system to track usage across time

## 📄 License

MIT License. Use it, fork it, improve it.

Built with ❤️ and memes by [@realquiller](https://github.com/realquiller)