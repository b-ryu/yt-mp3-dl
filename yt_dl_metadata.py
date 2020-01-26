# Script that unifies functionality between yt-mp3-dl and yt-metadata
#
# Args (in order):
# - destination/working folder
# - JSON file containing all downloading data/metadata
# - Album artwork mapping JSON


import os
import sys
import json
import re

from yt_mp3_dl import download_song
from yt_metadata import apply_mp3_metadata


def clean_filename(s):
    return re.sub(r'(?u)[^-\w.]', '', str(s).strip().replace(' ', '_'))


def generate_filename(data):
    if 'title' in data:
        return clean_filename(data.get('artist', '').replace(' ', '') + '_' + data['title'].replace(' ', '') + '.mp3')
    else:
        return clean_filename(data['yt_url'].replace('https://www.youtube.com/watch?v=', '') + '.mp3')


def yt_dl_metadata():
    # Validate args
    if len(sys.argv) < 3:
        print('Not enough arguments, see README for more details on usage')
        sys.exit(2)

    working_folder_path = sys.argv[1]
    metadata_path = sys.argv[2]

    if len(sys.argv) > 3:
        art_data_path = sys.argv[3]
    else:
        art_data_path = None

    if not os.path.isdir(working_folder_path):
        print('{dir} is not an existing directory'.format(dir=working_folder_path))
        sys.exit(1)
    elif not os.path.isfile(metadata_path):
        print('{file} is not an existing directory'.format(file=metadata_path))
        sys.exit(1)
    elif art_data_path is not None and not os.path.isfile(art_data_path):
        print('{file} is not an existing file, ignoring'.format(file=art_data_path))
        art_data_path = None

    # Read in files
    try:
        with open(metadata_path) as f:
            metadata = json.load(f)

        if not isinstance(metadata, list):
            print('MP3 metadata should be in the shape of a list of objects')
            sys.exit(1)
    except Exception as e:
        print('Could not read in {file}: {error}'.format(file=metadata_path, error=str(e)))
        sys.exit(1)

    if art_data_path:
        try:
            with open(art_data_path) as f:
                art_data = json.load(f)

            if not isinstance(art_data, dict):
                print('Album artwork map should be in the shape of a dict, ignoring')
                art_data = None
        except Exception as e:
            print('Could not read in {file}, ignoring: {error}'.format(file=art_data_path, error=str(e)))
            art_data = None
    else:
        art_data = None

    # For each object...
    successes = failures = 0
    metadata_changed = False

    for metadata_obj in metadata:
        try:
            # Get fields
            if 'filename' in metadata_obj:
                filename = metadata_obj['filename']  # name of destination file for download
            else:
                filename = generate_filename(metadata_obj)
                metadata_obj['filename'] = filename
                metadata_changed = True
            yt_url = metadata_obj['yt_url']  # link to YouTube video

            # Download MP3
            dl_result = download_song(working_folder_path, os.path.splitext(filename)[0], yt_url, lazy=True)

            if dl_result is False:
                raise Exception('Download failed')
            elif dl_result is None:
                print('MP3 file ({filename}) already exists, skipping metadata'.format(filename=filename))
            else:
                print('=================')

                # Set metadata/artwork
                apply_mp3_metadata(metadata_obj, working_folder_path, art_data)

                print('Successfully applied metadata for "{file}"'.format(file=filename))

                successes += 1
        except Exception as e:
            print('Could not download/set metadata for song specified by:\n{data}\nError: {error}'.format(
                data=str(metadata_obj),
                error=str(e)
            ))
            failures += 1

        print('#######################################################################################################')

    # Write album artwork data back to file
    if art_data_path and art_data:
        with open(art_data_path, 'w') as f:
            json.dump(art_data, f, indent=4)

    # Write metadata back to file, if changes were made
    if metadata and metadata_changed:
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4)

    print('Successfully downloaded and configured {s} songs'.format(s=successes))
    if failures:
        print('Failed to download or configure {f} songs'.format(f=failures))


if __name__ == '__main__':
    yt_dl_metadata()
