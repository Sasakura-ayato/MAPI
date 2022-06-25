# MAPI
Musiccasting API System (MAPI) 

> Last Update date : 2022/06/25 (1)

# Installation

## 1. 依存ライブラリのインストール
 
 ```
 cd MAPI
 pip3 install -r requirements.txt
 ```

 お好みによって `pyenv` を利用することも可能です。

## 2. データベースの初期化

```powershell
python3 init_database.py
```

# Usage

## Metadata to SQLite Database

### 1. データベースへ音楽の登録

```powershell
python3 import_meta.py

>>> Select Path :/Path/to/IncludedMusicFolder
>>> /path/to/IncludedMusicFolder/01 黙劇.mp4
>>> ...
>>> ('黙劇', '希織歌', 'HIMEHINA', 'HIMEHINA', '1', '1', 232.03958333333333, '/Path/to/IncludedMusicFolder/01 黙劇.mp4')
>>> ...
```

## MAPI endpoint

### 1. ウェブサーバーの起動

```powershell
cd app # MAPI/app に移動
uvicorn main:app 
```
`uvicorn main:app` に `--reload` オプションを付けると、app/main.py の上書き保存時に自動でサーバーを更新・再起動してくれるそうです。

### 現在の機能

すべて JSON で帰ってきます。

`success` が `true` か `false` で帰ってきていなければ、すべて想定していない挙動 = バグ。

> GET リクエスト ex.) `localhost:8000/query?type=title&q=曲名`

- `/` デバッグ用（API のバージョン ・ SQLite のバージョンの表示）
- `/query` 曲の検索（すべてあいまい検索）
    - `type` (Required) 検索対象のジャンル（タイトル・アルバム名など）
        - `title` タイトル（曲名）
        - `album` アルバム名
        - `artist` アーティスト名
        - `album_artist` アルバムアーティスト名
    - `q` (Required) 検索文字列