#!/usr/local/bin/python3

#
# Script for downloading batches of MP3s from YouTube using youtube-dl and FFmpeg executables
# Requires that youtube-dl and FFmpeg tools are on user's PATH
#
# YouTube doesn't support downloading MP3 straight up, so we download M4A and convert it using the FFmpeg utility
#


import sys
import os
import subprocess


def get_url_and_name(line):
    # line should in the format {youtube_url} | {file_name}
    yt_url, separator, filename = line.partition(' | ')

    if not separator:
        raise Exception('line is missing separator: {line}'.format(line=line))

    return yt_url.strip(), filename.strip()


def yt_mp3_dl():
    # Check arguments
    if len(sys.argv) != 3:
        print('Too many/few arguments; pass in a input file path and destination folder path to this script')
        sys.exit(2)

    input_file = sys.argv[1]
    dest_folder = sys.argv[2]

    if not os.path.isfile(input_file):
        print('{file} does not exist, please pass in a properly formatted existing file'.format(file=input_file))
        sys.exit(1)
    elif not os.path.isdir(dest_folder):
        print('{folder} does not exist, please pass in a existing destination directory'.format(folder=dest_folder))
        sys.exit(1)

    # Parse file
    try:
        with open(input_file) as f:
            url_name_pairs = [get_url_and_name(line) for line in f.readlines()]
    except Exception as e:
        print('Could not parse file; please check your formatting: {error}'.format(error=str(e)))
        sys.exit(1)

    # Begin downloads
    for url, name in url_name_pairs:
        download_song(dest_folder, name, url)
        print('================================================================')


def download_song(dest_folder, name, url, lazy=False):
    try:
        m4a_filepath = os.path.join(dest_folder, '{name}.m4a'.format(name=name))
        mp3_filepath = os.path.join(dest_folder, '{name}.mp3'.format(name=name))

        if os.path.isfile(m4a_filepath):
            raise Exception('There already exists an m4a file with name "{name}" in {dest}'.format(
                name=name, dest=dest_folder
            ))
        elif os.path.isfile(mp3_filepath):
            if lazy:
                print(
                    'There already exists an mp3 file with name "{name}" in {dest}. '
                    'Since "lazy" flag was set, assuming that '
                    'this is the MP3 we\'re looking for'.format(name=name, dest=dest_folder)
                )

                return None
            else:
                raise Exception(
                    'There already exists an mp3 file with name "{name}" in {dest}. '
                    'Since "lazy" flag was not set, assuming this is error'.format(name=name, dest=dest_folder)
                )

        # Download m4a from YouTube=
        subprocess.run([
            'youtube-dl', '-o', m4a_filepath, '-f' '140', url
        ], stdout=subprocess.DEVNULL)

        print('Downloaded "{name}" m4a file from YouTube'.format(name=name))

        # Convert m4a to mp3
        subprocess.run([
            'ffmpeg', '-i', m4a_filepath, '-acodec', 'libmp3lame', '-aq', '2', mp3_filepath
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print('Converted "{name}" from m4a to mp3'.format(name=name))

        # Delete m4a
        os.remove(m4a_filepath)

        print('Deleted "{name}" m4a file'.format(name=name))

        return True
    except Exception as e:
        print('Failed to download "{name}" mp3 from YouTube: {error}'.format(name=name, error=str(e)))

        return False


if __name__ == '__main__':
    yt_mp3_dl()
