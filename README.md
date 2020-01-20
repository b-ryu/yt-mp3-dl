# yt-mp3-dl

In addition to Python3, requires:
- `youtube-dl`
- `FFmpeg`

Both these tools should be on your `PATH`

### Usage
```
yt-mp3-dl <input file> <destination folder>
```

Input file contains the list of YouTube videos you'd like to convert to MP3
and download, as well as the corresponding filenames, formatting like so:

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
