from pathlib import Path


with open(Path(__file__).parent / "words.txt") as f:
    WORDS = f.readlines()

WORDS = [word.strip() for word in WORDS]
