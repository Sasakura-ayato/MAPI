from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
import os
import sqlite3
import glob

print('=== Metadata to SQLite Database v0.1.0a ===')

dbname = "MAPI_metadata.db"
conn = sqlite3.connect(dbname)
cur = conn.cursor()

# デバッグ用 ---
path = input("Select Path :")
# path = 'MusicAPI/13 リンクス_.mp4'
files = []
checked_files = []
files = glob.glob(path + "/*")

for file in files:
    extension = os.path.splitext(file)[1][1:]
    if (
        extension == "mp3"
        or extension == "mp4"
        or extension == "m4a"
        or extension == "flac"
    ):
        print(file)
        checked_files.append(file)


def extract(path):
    path = path.replace("\\", "/")
    extension = os.path.splitext(path)[1][1:]
    if extension == "mp3":
        mp3 = MP3(path)
        tags = mp3.tags
        info = mp3.info

        title = str(tags["TIT2"])
        album = str(tags["TALB"])
        artist = str(tags["TPE1"])
        album_artist = str(tags["TPE2"])
        track_number = str(tags["TRCK"])
        album_number = str(tags["TPOS"])
        length = info.length

        target = "/"
        track_number_idx = track_number.find(target)
        track_number = int(track_number[:track_number_idx])
        album_number_idx = album_number.find(target)
        album_number = int(album_number[:album_number_idx])
    elif extension == "mp4" or extension == "m4a":
        mp4 = MP4(path)
        tags = mp4.tags
        info = mp4.info

        title = str(tags["\xa9nam"][0])
        album = str(tags["\xa9alb"][0])
        artist = str(tags["\xa9ART"][0])
        album_artist = str(tags["aART"][0])
        track_number = str(tags["trkn"][0][0])
        album_number = str(tags["disk"][0][0])
        length = info.length
    elif extension == "flac":
        flac = FLAC(path)
        tags = flac.tags
        info = flac.info

        title = str(tags["title"][0])
        album = str(tags["album"][0])
        artist = str(tags["artist"][0])
        album_artist = str(tags["albumartist"][0])
        track_number = str(tags["tracknumber"][0])
        album_number = str(tags["discnumber"][0])
        length = info.length

        target = "/"
        album_number_idx = album_number.find(target)
        album_number = int(album_number[:album_number_idx])

    return title, album, artist, album_artist, track_number, album_number, length, path


for file in checked_files:
    values = str(extract(file))
    print(values)
    cur.execute(
        "INSERT INTO music_metadata(title, album, artist, album_artist, track_number, album_number, length, path) VALUES "
        + values
    )

conn.commit()
conn.close()
