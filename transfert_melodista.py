import glob
import os
import time

import requests

# Hello, you can change the values by yours

IPHONE_URL = "http://192.168.1.73/upload"
MUSIC_DIR = os.path.expanduser("~/BACKUP_FATRATRA/Spotify")
DONE_FILE = os.path.expanduser("~/BACKUP_FATRATRA/transfert_done.txt")
RETRY_DELAY = 5
MAX_RETRIES = 10

# Charge les fichiers déjà transférés
if os.path.exists(DONE_FILE):
    with open(DONE_FILE) as f:
        done = set(f.read().splitlines())
else:
    done = set()

mp3_files = sorted(glob.glob(os.path.join(MUSIC_DIR, "*.mp3")))
total = len(mp3_files)
remaining = [f for f in mp3_files if os.path.basename(f) not in done]

print(f"✓ {total} titres au total")
print(f"✓ {len(done)} déjà transférés")
print(f"→ {len(remaining)} restants\n")

for i, filepath in enumerate(remaining, 1):
    filename = os.path.basename(filepath)
    print(f"[{i}/{len(remaining)}] {filename[:60]}...")

    retries = 0
    success = False

    while retries < MAX_RETRIES:
        try:
            with open(filepath, "rb") as f:
                response = requests.post(
                    IPHONE_URL,
                    files={"files[]": (filename, f, "audio/mpeg")},
                    timeout=60,
                )
            if response.status_code in (200, 201, 204):
                print(f"  ✓ OK")
                with open(DONE_FILE, "a") as done_f:
                    done_f.write(filename + "\n")
                success = True
                break
            else:
                print(
                    f"  ✗ Erreur HTTP {response.status_code}, retry {retries + 1}/{MAX_RETRIES}"
                )
        except Exception as e:
            print(
                f"  ✗ Connexion perdue ({e}), retry dans {RETRY_DELAY}s... ({retries + 1}/{MAX_RETRIES})"
            )
            time.sleep(RETRY_DELAY)

        retries += 1
        time.sleep(2)

    if not success:
        print(f"  ✗ Echec définitif pour {filename}")

print(f"\n✓ Transfert terminé !")
print(f"Pour reprendre si interruption : python3 transfert_melodisata.py")
