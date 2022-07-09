# https://qiita.com/yota_dev/items/ab8dea7f71c8a130d5bf

from ast import While
import logging
from cv2 import detail_BlocksGainCompensator
from fastapi import FastAPI
from typing import Union
import datetime
import sqlite3
import vlc

# API サーバーの起動
app = FastAPI()
version = "1.0.0"

# VLC インスタンスの起動
p = vlc.MediaPlayer()
pl = [
    "C:\\Users\\______\\source\\MAPI\\MusicAPI\\1-03 ambivalent world_.mp4",
    "C:\\Users\\______\\source\\MAPI\\MusicAPI\\1-03 - 鳥の詩.m4a",
]
index = 0

# Uvicorn Access Logger
logging.basicConfig(filename="./log.txt", level=logging.DEBUG)


# 標準エラーメッセージの定義
def success_message(message: str = "Success"):
    return {
        "success": "true",
        "version": version,
        "ReceivingDate": datetime.datetime.now(),
        "message": message,
    }


def failed_empty_parameters_message(parameters: str = "Failed"):
    return {
        "success": "false",
        "version": version,
        "ReceivingDate": datetime.datetime.now(),
        "message": "parameter " + parameters + " is(are) empty.",
    }


# VLC 独自拡張関数


def play_list(pl: str = None, select_track: int = None):
    global index
    if select_track != None:
        index = select_track
    if pl == None:
        return failed_empty_parameters_message("`pl`")
    p.set_mrl(pl[index])
    p.play()


# @get Music Database


def cv_dict(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.get("/")
async def root(q: Union[str, None] = None):
    dbname = "../MAPI_metadata.db"
    conn = sqlite3.connect(dbname)
    conn.row_factory = cv_dict
    cur = conn.cursor()
    cur.execute("select count(*) from music_metadata;")
    result = cur.fetchall()
    return {
        "message": "Hello World!",
        "version": version,
        "ReceivingDate": datetime.datetime.now(),
        "message": "This endpoint is debug attribute.",
        "q": q,
        "sqlite3 Version": sqlite3.sqlite_version,
        "amount of songs": result,
    }


@app.get("/query")
async def root(type: Union[str, None] = None, q: Union[str, None] = None):
    dbname = "../MAPI_metadata.db"
    conn = sqlite3.connect(dbname)
    conn.row_factory = cv_dict
    cur = conn.cursor()

    if type == None or q == None:
        return failed_empty_parameters_message("`type` or `q`")

    cur.execute("SELECT * FROM music_metadata WHERE " + type + " LIKE '%" + q + "%'")
    result = cur.fetchall()
    conn.close()

    return {
        "success": "true",
        "version": version,
        "ReceivingDate": datetime.datetime.now(),
        "data": result,
    }


# @get/post VLC Instance


@app.get("/vlc/status")
async def root(type: Union[str, None] = None):
    global index
    return {
        "status": {
            "success": "true",
            "version": version,
            "ReceivingDate": datetime.datetime.now(),
        },
        "is_playing": str(p.is_playing()),
        "Now_playing": {
            "track_index": index,
            "current_time": str(p.get_time()),
            "current_time_length": str(p.get_length()),
            "title": p.get_title(),
            "get_role": p.get_role(),
            "audio_channel": str(p.audio_get_channel()),
            "current_volume": str(p.audio_get_volume()),
        },
        "mrl_queue": pl,
    }


@app.get("/vlc/playlist")
async def root():
    return pl


@app.post("/vlc/add")
async def root(path: Union[str, None] = None):
    if path == None:
        return failed_empty_parameters_message("`path`")
    pl.append(path)
    return success_message("Add datum path")


@app.post("/vlc/play")
async def root():
    play_list(pl)
    return success_message("[VLC]: Start")


@app.post("/vlc/stop")
async def root():
    p.stop()
    return success_message("[VLC]: Stop")


@app.post("/vlc/prev")
async def root():
    global index
    index = index - 1
    p.set_mrl(pl[index])
    p.play()
    return success_message("[VLC]: Previous")


@app.post("/vlc/time")
async def root(time: Union[int, None] = None):
    if time == None:
        return failed_empty_parameters_message("`time[ms]`")
    p.set_time(time)
    return success_message("[VLC]: Time: " + str(time))


@app.post("/vlc/next")
async def root():
    global index
    index = index + 1
    p.set_mrl(pl[index])
    p.play()
    return success_message("[VLC]: Next")


@app.post("/vlc/volume")
async def root(value: Union[int, None] = 0):
    p.audio_set_volume(value)
    return success_message("[VLC]: Volume Change: " + str(value))
