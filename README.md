These are some Python scripts I wrote for batch downloading/managing MP3 files from YouTube (WIP).

- **`yt-mp3-dl`**: for batch downloading MP3 from YouTube
- **`yt-metadata`**: for batch managing metadata for MP3 files
- **`yt-dl-metadata`**: combines the functionality of the previous two scripts into one
  (TODO: update README)

# yt-mp3-dl

In addition to Python3, requires:

- [`youtube-dl`](https://ytdl-org.github.io/youtube-dl/index.html)
- [`FFmpeg`](https://www.ffmpeg.org/)

Both these tools should be on your `PATH`.

### Usage

```
yt_mp3_dl <input file> <destination folder>
```

Input file contains the list of YouTube videos you'd like to convert to MP3
and download, as well as the corresponding filenames, formatted like so:

```
<youtube url> | <file name>
<youtube url> | <file name>
<youtube url> | <file name>
...
```

For example, if my input file is `input.txt` and contains

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ | some innocuous song
```

and I run `yt-mp3-dl input.txt /Users/myname/Music`,
the script should download and convert the video's audio and place it at
`/Users/myname/Music/some innocuous song.mp3`

# yt-metadata

Before using this script you need to install dependencies using

```
pip install -r requirements.txt
```

### Usage

```
python3 yt_metadata <mp3 folder> <metadata config> <album art map (optional)>
```

`mp3 folder` is the path to the folder on your computer containing the MP3 files you want to modify.
`metadata config` is the path to the JSON config file that has all the metadata.
See below for more details on the optional `album art map` parameter.

### Config structure

`metadata config` should contain a well-formatted array of JSON objects, each one containing the metadata
for a different MP3 file. For example, the following JSON contains the metadata for a single MP3 file called
`test.mp3`

```
[
  {
    "filename": "test.mp3",
    "artist": "Michael Jackson",
    "title": "Thriller",
    "album": "Thriller",
    "album_artist": "Michael Jackson"
  }
]
```

Only `filename` is required, the rest will be set if they are available.
The fields in the metadata object are identical to their counterparts
specified by the [`eyeD3` API](https://eyed3.readthedocs.io/en/latest/_modules/eyed3/id3/tag.html).

### Adding album cover art to your MP3

There are several ways you can configure your script to add album art to your MP3 files.
The script looks for each of the following in order until it finds a suitable image, if at all.

1. Include a `song_art_path` or `album_art_path` in your metadata object. The value should be either an absolute (or relative
   to the script's working directory) path to the image file you'd like to embed as cover art.
   `{ "filename": "test.mp3", "artist": "Michael Jackson", "title": "Thriller", "album": "Thriller", "album_artist": "Michael Jackson", "song_art_path": "/Users/my_user/Images/thriller_cover_art.jpg" }`
2. Include a `song_art_url` or `album_art_url` in your metadata object. The value should a URL to the image resource you'd like
   to embed as your cover art.
   `{ "filename": "test.mp3", "artist": "Michael Jackson", "title": "Thriller", "album": "Thriller", "album_artist": "Michael Jackson", "song_art_url": "https://upload.wikimedia.org/wikipedia/en/5/55/Michael_Jackson_-_Thriller.png" }`
3. If either of these fields are omitted, and you passed in a path to `album art map` JSON config earlier
   (see usage details above), then the script will look through it to see if it contains details on
   what image it should use. `album art map` should be path to a JSON file structured something like below:
   `{ "Michael Jackson - Thriller": { "path": "/Users/my_user/Images/thriller_cover_art.jpg", "url": "https://upload.wikimedia.org/wikipedia/en/5/55/Michael_Jackson_-_Thriller.png" } }`
   The key should be structured as `<album artist (or artist)> - <album name>`. The value is a object
   containing either `path` or `url` fields (or both, but the script will default to `path`) pointing to
   an image file to use as cover art (similar to the previous two options).
   This may be useful
   if you are embedding metadata and album art for a bunch of songs from the same album, and don't feel like
   copying in a `path` or `url` field into each of the song's metadata objects. Instead you can set it once
   and have it be applied to every song the script recognizes as being part of that album.
