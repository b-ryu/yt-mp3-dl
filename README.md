# yt-mp3-dl

These are some Python scripts I wrote for downloading/managing MP3 files from YouTube.

- **`yt-mp3-dl`**: for downloading MP3 files from YouTube videos
- **`yt-metadata`**: for managing metadata for MP3 files

## Contents

- [`yt-mp3-dl`](#dl)
  - [Requirements](#dl-req)
  - [Usage](#dl-usage)
- [`yt-metadata`](#meta)
  - [Requirements](#meta-req)
  - [Usage](#meta-usage)
    - [Metadata config](#meta-usage-meta)
    - [Cover art config](#meta-usage-art)

## <a name="dl"></a> `yt-mp3-dl`

### <a name="dl-req"></a> Requirements

Requires Python 3.

`yt-mp3-dl` requires that you have these programs on your path:

- [`youtube-dl`](https://ytdl-org.github.io/youtube-dl/index.html)
- [`FFmpeg`](https://www.ffmpeg.org/)

### <a name="dl-usage"></a> Usage

```sh
python3 yt_mp3_dl.py <input-file> <dest-folder> [--lazy] [--clean]
```

`<input-file>` should be a path (relative or absolute) to a file formatted like so:

```
https://www.youtube.com/watch?v=FveF-we6lcE | monke
https://www.youtube.com/watch?v=KMU0tzLwhbE | developers
https://www.youtube.com/watch?v=dQw4w9WgXcQ | trust-me
```

`<dest-folder>` should be a path to an existing folder in which the MP3 files will be placed.

Thus if I ran `python3 yt_mp3_dl.py input.txt songs` with the above inputs, I would expect to find

- `./songs/monke.mp3`,
- `./songs/developers.mp3`, and
- `./songs/trust-me.mp3`

in my `songs` folder afterwards (assuming the script, file, and folder are in the same directory).

The flags `--lazy` and `--clean` do the following:

- `--lazy`: if set, then the script will not overwrite existing files of the same name (default behaviour)
- `--no-clean`: if set, will leave `.m4a` download files instead of deleting them afterwards (default behaviour)

## <a name="meta"></a> `yt-metadata`

### <a name="meta-req"></a> Requirements

Requires Python 3.

Run the following (or equivalent) to install the Python dependencies:

```sh
pip install -r requirements.txt
```

### <a name="meta-usage"></a> Usage

```sh
python3 yt_metadata.py <mp3-folder> <metadata-config> [<cover-art-config>]
```

`<mp3-folder>` should be a path to the folder containing your MP3 files whose metadata you wish to modify.

`<metadata-config>` should be a path to JSON config containing your metadata for those files. [More details below](#meta-usage-meta).

You can also optionally pass in a `<cover-art-config>`, which should be a path to JSON config detailing the cover art for those files. [More details below](#meta-usage-art).

#### <a name="meta-usage-meta"></a> Metadata config

A metadata config is a JSON file containing an array of objects detailing the song metadata for a MP3 file. Below is an example config for one song:

```json
[]
```

Only the `filename` field is required. The config supports fields in the ID3 spec as described in the [`eyeD3` API]().

#### <a name="meta-usage-art"></a> Cover art config

A cover art config is another JSON config that helps configure album art for specific albums. Instead of adding/removing cover art fields for each song in a specific album, you can write a single album entry in this config and pass it to `yt_metadata`. For instance:

```json
{}
```
