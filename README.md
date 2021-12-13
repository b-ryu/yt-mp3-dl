# yt-mp3-dl

These are some Python scripts I wrote for downloading/managing MP3 files from YouTube.

- **`yt-mp3-dl`**: for downloading MP3 files from YouTube videos
- **`yt-metadata`**: for managing metadata for MP3 files

## Contents

- [`yt-mp3-dl`](#yt-mp3-dl)
  - [Requirements](#yt-mp3-dl-requirements)
  - [Usage](#yt-mp3-dl-usage)
- [`yt-metadata`](#yt-metadata)
  - [Requirements](#yt-metadata-requirements)
  - [Usage](#yt-metadata-usage)
    - [Metadata config](#metadata-config)
    - [Cover art config](#cover-art-config)

## `yt-mp3-dl`

### `yt-mp3-dl` requirements

Requires Python 3.

`yt-mp3-dl` requires that you have these programs on your `PATH`:

- [`youtube-dl`](https://ytdl-org.github.io/youtube-dl/index.html)
- [`FFmpeg`](https://www.ffmpeg.org/)

### `yt-mp3-dl` usage

```sh
python3 yt-mp3-dl.py <input-file> <dest-folder> [--lazy] [--clean]
```

`<input-file>`: path to a list of YouTube URLs and destination names, formatted like so:

```
https://www.youtube.com/watch?v=FveF-we6lcE | monke
https://www.youtube.com/watch?v=KMU0tzLwhbE | developers
https://www.youtube.com/watch?v=dQw4w9WgXcQ | trust-me
```

`<dest-folder>`: path to a destination folder

The flags `--lazy` and `--clean` do the following:

- `--lazy`: if set, then the script will not overwrite existing files of the same name (default behaviour)
- `--no-clean`: if set, will leave `.m4a` download files instead of deleting them afterwards

## `yt-metadata`

### `yt-metadata` requirements

Requires Python 3.

Run the following (or equivalent) to install the Python dependencies:

```sh
pip install -r requirements.txt
```

### `yt-metadata` usage

```sh
python3 yt-metadata.py <mp3-folder> <metadata-config> [<cover-art-config>]
```

`<mp3-folder>` should be a path to the folder containing your MP3 files whose metadata you wish to modify.

`<metadata-config>` should be a path to JSON config containing your metadata for those files. [More details below](#meta-usage-meta).

You can also optionally pass in a `<cover-art-config>`, which should be a path to JSON config detailing the cover art for those files. [More details below](#meta-usage-art).

#### Metadata config

A metadata config is a JSON file containing an array of objects detailing the song metadata for a MP3 file. Below is an example config for one song:

```json
{}
```

Only the `filename` field is required. The config supports fields in the ID3 spec as described in the [`eyeD3` API]().

#### Cover art config

A cover art config is another JSON config that helps configure album art for specific albums. Instead of adding/removing cover art fields for each song in a specific album, you can write a single album entry in this config and pass it to `yt_metadata`. For instance:

```json
{}
```
