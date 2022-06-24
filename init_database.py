import sqlite3

dbname = "MAPI_metadata.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()
cur.execute(
    "CREATE TABLE music_metadata(id INTEGER PRIMARY KEY AUTOINCREMENT, title STRING, album STRING, artist STRING, album_artist STRING, track_number INTEGER, album_number INTEGER, length REAL, path STRING)"
)

conn.close()
