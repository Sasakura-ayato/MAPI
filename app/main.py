# https://qiita.com/yota_dev/items/ab8dea7f71c8a130d5bf

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

# 標準エラーメッセージの定義
def success_message(message: str = 'Success'):
    return {
        "success": "true",
        "version": version,
        "ReceivingDate": datetime.datetime.now(),
        "message": message
    }

def failed_empty_parameters_message(parameters: str = 'Failed'):
    return {
        "success": "false",
        "version": version,
        "ReceivingDate": datetime.datetime.now(),
        "message": "parameter " + parameters + " is(are) empty.",
    }



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
        "message": "This endpoint is debug system.",
        "q": q,
        "sqlite3 Version": sqlite3.sqlite_version,
        "amount of songs": result
    }


@app.get("/query")
async def root(type: Union[str, None] = None, q: Union[str, None] = None):
    dbname = "../MAPI_metadata.db"
    conn = sqlite3.connect(dbname)
    conn.row_factory = cv_dict
    cur = conn.cursor()

    if type == None or q == None:
        return failed_empty_parameters_message('`type` or `q`')

    cur.execute("SELECT * FROM music_metadata WHERE " + type + " LIKE '%" + q + "%'")
    result = cur.fetchall()
    conn.close()

    return {
        "success": "true",
        "version": version,
        "ReceivingDate": datetime.datetime.now(),
        "data": result,
    }

@app.get("/status")
async def root(type: Union[str, None] = None):
    status = p.get_media_player()
    return {
        "track-index": status.get_media(),
        "time": str(status.get_time() / 1000),
        "mrl": status.get_mrl()
    }

@app.post("/vlc/play")
async def root(path: Union[str, None] = None):
    if path == None:
        return failed_empty_parameters_message('`path`')

    p.set_mrl(path)
    p.play()

    return success_message("VLC Started")

@app.post("/vlc/stop")
async def root():
    p.stop()
    return success_message("VLC Stopped")