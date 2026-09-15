import sqlite3
import re

conn = sqlite3.connect('data/quran.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS morphology (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah INTEGER,
    ayah INTEGER,
    word INTEGER,
    segment INTEGER,
    arabic TEXT,
    pos TEXT,
    root TEXT,
    lemma TEXT,
    features TEXT
)''')

with open('data/quran-morphology.txt', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) < 4:
            continue
        loc = parts[0].strip('()')
        s, a, w, seg = loc.split(':')
        arabic = parts[1]
        pos = parts[2]
        feat_str = parts[3]
        root_match = re.search(r'ROOT:(\S+?)(\||$)', feat_str)
        lem_match = re.search(r'LEM:(\S+?)(\||$)', feat_str)
        root = root_match.group(1) if root_match else None
        lemma = lem_match.group(1) if lem_match else None
        c.execute('''INSERT INTO morphology
            (surah, ayah, word, segment, arabic, pos, root, lemma, features)
            VALUES (?,?,?,?,?,?,?,?,?)''',
            (int(s), int(a), int(w), int(seg), arabic, pos, root, lemma, feat_str))

conn.commit()
print("Selesai. Total baris:", c.execute("SELECT COUNT(*) FROM morphology").fetchone()[0])
conn.close()

