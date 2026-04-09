# spotify-playlist-exporter

Download your entire Spotify playlist as MP3 files with embedded metadata and cover art — no Spotify subscription required.

## The problem

I cancelled my Spotify subscription but had 539 songs in my playlist I didn't want to lose. Every export site online is limited to 3–5 tracks. spotDL kept throwing errors. The Spotify API rate limits without Premium. YouTube Music blocks automated requests.

So I wrote this script.

## How it works

1. Export your Spotify playlist as a CSV using [exportify.net](https://exportify.net)
2. Run the script — it reads every track from the CSV, searches YouTube, and downloads each one as MP3 with cover art and metadata embedded

No Spotify API key needed. No Premium subscription. Just Python and yt-dlp.

## Requirements

```bash
# Python 3.12 recommended (3.14 has compatibility issues with some deps)
python3.12 -m venv env
source env/bin/activate
pip install yt-dlp
sudo pacman -S ffmpeg   # Arch Linux
# or: sudo apt install ffmpeg
```

## Usage

1. Go to [exportify.net](https://exportify.net), log in with Spotify and export your playlist as CSV
2. Place the CSV in the project folder and rename it `playlist.csv`
3. Run:

```bash
python3 download_playlist.py
```

MP3 files are saved to `~/BACKUP/Spotify/` by default. Failed downloads are logged to `erreurs.txt`.

## Output

Each track is downloaded with:
- embedded cover art
- title and artist metadata
- 320kbps quality (best available)

Works great with the native Apple Music app on iPhone — just sync via iTunes/Finder or transfer wirelessly with VLC.

## Stack

- Python 3.12
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- ffmpeg
- [exportify.net](https://exportify.net) for the initial CSV export

## Why

Because the best motivation to learn is being too broke to pay for another subscription.