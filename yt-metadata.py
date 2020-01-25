#
# Script for batch modifying MP3 file metadata using JSON configs
# Make sure that you "pip install -r requirements.txt" before running this script, as it relies
# on third-party libraries (i.e. eyeD3)
#


import sys
import json
import os
from urllib.request import urlopen

import eyed3


def apply_metadata_tag(mp3_file, tag_name, data, fallback_tag_name=None):
    tag_value = data.get(tag_name, data.get(fallback_tag_name) if fallback_tag_name else None)

    if not tag_value:
        return

    setattr(mp3_file.tag, tag_name, tag_value)


def get_mime_type(url_or_path):
    mime_map = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png'
    }
    mime_type = None

    for file_ext in mime_map:
        if url_or_path.endswith(file_ext):
            mime_type = mime_map[file_ext]

    return mime_type


def apply_cover_art_from_file(mp3_file, filepath):
    # Check that file exists
    if not os.path.isfile(filepath):
        print('{file} is not an existing file and cannot be used for cover art'.format(file=filepath))
        return False

    # Get MIME type
    mime_type = get_mime_type(filepath)

    if mime_type is None:
        print('{file} is not of MIME type image/jpeg or image/png. Please select an image of those types'.format(
            file=filepath
        ))
        return False

    # Set cover art
    try:
        mp3_file.tag.images.set(3, open(filepath, 'rb').read(), mime_type)
    except Exception as e:
        print('Could not set {file} as cover art: {error}'.format(file=filepath, error=str(e)))
        return False

    return True


def apply_cover_art_from_url(mp3_file, url):
    try:
        response = urlopen(url)
        image_data = response.read()
        mime_type = response.info().get_content_type()

        mp3_file.tag.images.set(
            type_=3,
            img_data=image_data,
            mime_type=mime_type,
        )
    except Exception as e:
        print('Could not set {url} as cover art: {error}'.format(url=url, error=str(e)))
        return False

    return True


def apply_cover_art_from_map(mp3_file, data, art_map):
    key = '{artist} - {album_name}'.format(
        artist=data.get('album_artist', data['artist']),
        album_name=data['album']
    )

    if key in art_map:
        album_art_data = art_map[key]

        if 'path' in album_art_data:
            if apply_cover_art_from_file(mp3_file, album_art_data['path']):
                return True

        if 'url' in album_art_data:
            if apply_cover_art_from_url(mp3_file, album_art_data['url']):
                return True

    return False


def set_album_cover_art(mp3_file, data, art_map=None):
    # Check for files on computer
    if 'cover_art_path' in data:
        if apply_cover_art_from_file(mp3_file, data['cover_art_path']):
            return

    # Check for URLs
    if 'cover_art_url' in data:
        if apply_cover_art_from_url(mp3_file, data['cover_art_url']):
            return

    # Check map
    if art_map and 'album' in data and ('artist' in data or 'album_artist' in data):
        if apply_cover_art_from_map(mp3_file, data, art_map):
            return

    return


def apply_mp3_metadata(data, folder, cover_art=None):
    mp3_file_path = os.path.join(folder, data['filename'])

    if not os.path.isfile(mp3_file_path):
        raise Exception('{file} does not exist'.format(file=mp3_file_path))
    elif not mp3_file_path.endswith('.mp3'):
        raise Exception('{file} does not appear to be an MP3 file'.format(file=mp3_file_path))

    mp3_file = eyed3.load(mp3_file_path)

    apply_metadata_tag(mp3_file, 'artist', data)
    apply_metadata_tag(mp3_file, 'title', data)
    apply_metadata_tag(mp3_file, 'album', data)
    apply_metadata_tag(mp3_file, 'album_artist', data, 'artist')

    set_album_cover_art(mp3_file, data, cover_art)

    mp3_file.tag.save()


if __name__ == '__main__':
    # Check arguments
    if len(sys.argv) < 3:
        print('Too few arguments; pass in at least a MP3 file folder and JSON config path to this script')
        sys.exit(2)

    mp3_folder = sys.argv[1]
    json_config = sys.argv[2]
    if len(sys.argv) > 3:
        cover_art_map_file = sys.argv[3]
    else:
        cover_art_map_file = None

    # Check that folder and file exist
    if not os.path.isfile(json_config) or not os.path.isdir(mp3_folder):
        print('Either {dir} is not an existing directory or {file} is not an existing file'.format(
            dir=mp3_folder, file=json_config
        ))
        sys.exit(1)
    elif cover_art_map_file is not None and not os.path.isfile(cover_art_map_file):
        print('{file} is not an existing file, ignoring cover art map'.format(file=cover_art_map_file))
        cover_art_map_file = None

    # Parse JSON
    # This file will contain all the metadata you'd like to apply to your MP3 files
    try:
        with open(json_config) as f:
            mp3_metadata = json.load(f)
    except Exception as e:
        print('Could not load JSON config: {error}'.format(error=str(e)))
        sys.exit(1)

    if cover_art_map_file:
        try:
            with open(cover_art_map_file) as f:
                cover_art_map = json.load(f)
        except Exception as e:
            print('Could not load cover art map, skipping: {error}'.format(error=str(e)))
            cover_art_map_file = None
    else:
        cover_art_map = None

    # Check shape of data
    if not isinstance(mp3_metadata, list):
        print('Your MP3 metadata JSON object should be a list of properly formatted objects, see README.md for details')
        sys.exit(1)
    elif cover_art_map is not None and not isinstance(cover_art_map, dict):
        print('Your cover art JSON map should be shaped like a dict, see README.md for details, ignoring')
        cover_art_map = None

    # Iterate through metadata object and apply metadata to MP3 file
    successes = failures = 0

    for metadata in mp3_metadata:
        try:
            apply_mp3_metadata(metadata, mp3_folder, cover_art_map)
            print('Successfully applied metadata for {file}'.format(file=metadata.get('filename')))
            successes += 1
        except Exception as e:
            print('Could not apply metadata specified by this object:\n{metadata}\nError: {error}'.format(
                metadata=metadata, error=str(e)
            ))
            failures += 1

        print('==================================================================')

    print('Successfully applied metadata to {s} files'.format(s=successes))
    if failures:
        print('Failed to apply metadata to {f} files'.format(f=failures))
