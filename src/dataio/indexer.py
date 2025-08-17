import os
import csv
import re
from src.paths import DATASET_ROOT,METADATA_CSV

# Regex to parse filenames like: 123__M_Left_index_finger
filename_re = re.compile(r"(?P<id>\d+)__([MF])_(?P<hand>Left|Right)_(?P<finger>\w+)")

# Metadata header
header = ["person_id", "hand", "finger", "difficulty", "alteration", "filename", "filepath"]

rows = []

for person in os.listdir(DATASET_ROOT):
    person_dir = os.path.join(DATASET_ROOT, person)
    if not os.path.isdir(person_dir):
        continue

    # person_<number>
    person_id = person.replace("person_", "")

    for difficulty in os.listdir(person_dir):
        difficulty_dir = os.path.join(person_dir, difficulty)
        if not os.path.isdir(difficulty_dir):
            continue

        # Special case: original images (no alteration)
        if difficulty.lower() == "original":
            for fname in os.listdir(difficulty_dir):
                match = filename_re.match(fname)
                if not match:
                    continue
                row = [
                    match.group("id"),
                    match.group("hand"),
                    match.group("finger"),
                    "original",
                    "none",
                    fname,
                    os.path.join(difficulty_dir, fname)
                ]
                rows.append(row)
            continue

        # Altered folders (Easy, Medium, Hard)
        for alteration in os.listdir(difficulty_dir):
            alteration_dir = os.path.join(difficulty_dir, alteration)
            if not os.path.isdir(alteration_dir):
                continue

            for fname in os.listdir(alteration_dir):
                match = filename_re.match(fname)
                if not match:
                    continue
                row = [
                    match.group("id"),
                    match.group("hand"),
                    match.group("finger"),
                    difficulty.replace("Altered_", "").lower(),
                    alteration,
                    fname,
                    os.path.join(alteration_dir, fname)
                ]
                rows.append(row)

# Write CSV
with open(METADATA_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"Metadata saved to {METADATA_CSV}, total {len(rows)} samples.")
