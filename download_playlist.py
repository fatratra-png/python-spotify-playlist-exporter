
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

CSV_FILE = os.path.expanduser("~/Téléchargements/playlist.csv")
#If you cloned my repo,use your own path to the csv file, or move the csv file to the path above and rename it to playlist.csv
#Use Exportify to export your Spotify playlist to a csv file, then move it to the path above and rename it to playlist.csv(yeah better to use an short and useful name), or change the CSV_FILE variable to point to your csv file. The csv file should have two columns: "Nom du titre" and "Nom(s) de l'artiste", which correspond to the title of the track and the name of the artist(s) respectively.
OUTPUT_DIR = os.path.expanduser("~/BACKUP_FATRATRA/Spotify")
ERRORS_FILE = os.path.join(OUTPUT_DIR, "erreurs.txt")

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(CSV_FILE, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    tracks = [(row["Nom du titre"], row["Nom(s) de l'artiste"]) for row in reader]

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
