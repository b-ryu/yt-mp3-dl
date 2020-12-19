# yt-mp3-dl

These are some Python scripts I wrote for batch downloading/managing MP3 files from YouTube.

- **`yt-mp3-dl`**: for batch downloading MP3 from YouTube
- **`yt-metadata`**: for batch managing metadata for MP3 files
- **`yt-dl-metadata`**: combines the functionality of the other two scripts

## Contents

- [`yt-mp3-dl`](#dl)
  - [Requirements](#dl-req)
  - [Usage](#dl-usage)
- [`yt-metadata`](#meta)
  - [Requirements](#meta-req)
  - [Usage](#meta-usage)
- [`yt-dl-metadata`](#comb)
  - [Requirements](#comb-req)
  - [Usage](#comb-usage)

## <a name="dl"></a> `yt-mp3-dl`

### <a name="dl-req"></a> Requirements

Requires Python 3.

`yt-mp3-dl` requires that you have these programs on your path:

- [`youtube-dl`](https://ytdl-org.github.io/youtube-dl/index.html)
- [`FFmpeg`](https://www.ffmpeg.org/)

### <a name="dl-usage"></a> Usage

```sh
python3 yt_mp3_dl.py <input-file> <dest-folder>
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

## <a name="meta"></a> `yt-metadata`

### <a name="meta-req"></a> Requirements

### <a name="meta-usage"></a> Usage

## <a name="comb"></a> `yt-dl-metadata`

### <a name="comb-req"></a> Requirements

### <a name="comb-usage"></a> Usage
