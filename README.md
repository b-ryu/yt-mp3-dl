These are some Python scripts I wrote for batch downloading/managing of MP3 files from YouTube (**WIP**).

# yt-mp3-dl

In addition to Python3, requires:
- [`youtube-dl`](https://ytdl-org.github.io/youtube-dl/index.html)
- [`FFmpeg`](https://www.ffmpeg.org/)

Both these tools should be on your `PATH`

### Usage
```
yt-mp3-dl <input file> <destination folder>
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
python3 yt-metadata <mp3 folder> <metadata config>
```
`mp3 folder` is the path to the folder on your computer containing the MP3 files you want to modify.
`metadata config` is the path to the JSON config file that has all the metadata.

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
The fields in the metadata object are identical to their counterparts 
specified by the [`eyeD3` API](https://eyed3.readthedocs.io/en/latest/_modules/eyed3/id3/tag.html).
Right now the above fields are the only ones supported, but I plan on adding more.