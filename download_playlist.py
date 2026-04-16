
#ALGORITHM

#PROBLEM ANALYSIS
#Input: A CSV file containing the title and artist of each track in a Spotify playlist.
#Output: MP3 files of each track downloaded from YouTube, saved in a specified output directory. If any track fails to download, its title and artist will be saved in an errors.txt

#APPROACH
#1. Read the CSV file and extract the title and artist of each track.
#2. For each track, construct a search query combining the artist and title.
#3. Use yt-dlp to search YouTube for the track and download the audio in MP3 format, embedding the thumbnail and adding metadata.
#4. Save the downloaded files in the specified output directory.
#5. If any track fails to download, log the error in a text file.   

#PSEUDOCODE


#IMPLEMENTATION:

import csv
import subprocess
import sys
import os

CSV_FILE = os.path.expanduser("./playlist.csv")
# Create a directory for downloaded music
os.makedirs(os.path.expanduser("~/Spotify"), exist_ok=True)
OUTPUT_DIR = os.path.expanduser("~/Spotify")
ERRORS_FILE = os.path.join(OUTPUT_DIR, "erreurs.txt")

TITLE_COLUMNS = [
    "Nom du titre",
    "Track Name",
    "Title"
]

ARTIST_COLUMNS = [
    "Nom(s) de l'artiste",
    "Artist Name(s)",
    "Artist"
]

def find_column(headers: list[str], candidates: list[str]) -> str | None:
    for candidate in candidates:
        if candidate in headers:
            return candidate
    return None

with open(CSV_FILE, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames or []

    title_col = find_column(headers, TITLE_COLUMNS)
    artist_col = find_column(headers, ARTIST_COLUMNS)

    if not title_col or not artist_col:
        print(f"Erreur: Colonnes non trouvées dans le CSV.")
        print(f"Colonnes disponibles: {headers}")
        sys.exit(1)

    tracks = [(row[title_col], row[artist_col]) for row in reader]

print(f"✓ {len(tracks)} titres trouvés dans la playlist\n")

errors = []

for i, (title, artist) in enumerate(tracks, 1):
    query = f"{artist} - {title}"
    print(f"[{i}/{len(tracks)}] Téléchargement : {query}")

    cmd = [
        "yt-dlp",
        f"ytsearch1:{query}",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--embed-thumbnail",
        "--add-metadata",
        "--parse-metadata", f":{artist}:%(artist)s",
        "--output", os.path.join(OUTPUT_DIR, "%(title)s.%(ext)s"),
        "--no-playlist",
        "--quiet",
        "--no-warnings",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  ✗ Erreur : {query}")
        errors.append(query)
    else:
        print(f"  ✓ OK")

print(f"\n✓ Terminé ! {len(tracks) - len(errors)}/{len(tracks)} titres téléchargés.")

if errors:
    with open(ERRORS_FILE, "w") as f:
        f.write("\n".join(errors))
    print(f"✗ {len(errors)} erreurs sauvegardées dans {ERRORS_FILE}")
