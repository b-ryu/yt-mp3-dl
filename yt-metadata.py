import sys
import json
import os
from urllib.request import urlopen

import eyed3

# #################################################################################################
# Logging helpers
# #################################################################################################

DIVIDER = '==============================================================='

def log(s):
    print('[YT-METADATA LOG]: {}'.format(s))

def error(s):
    print('[YT-METADATA ERROR]: {}'.format(s))

# #################################################################################################
# Validators
# #################################################################################################

def is_list(l):
    return isinstance(l, list)

def is_dict(d):
    return isinstance(d, dict)

# #################################################################################################
# Helpers
# #################################################################################################

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
    key = get_album_art_data_key(data)

    if key in art_map:
        album_art_data = art_map[key]

        if 'path' in album_art_data:
            if apply_cover_art_from_file(mp3_file, album_art_data['path']):
                return True

        if 'url' in album_art_data:
            if apply_cover_art_from_url(mp3_file, album_art_data['url']):
                return True

    return False

def add_album_art_data(art_map, data, path=None, url=None):
    if art_map is None or data is None or (path is None and url is None):
        return

    art_map_key = get_album_art_data_key(data)
    album_art_data = art_map.get(art_map_key, {})

    if path is not None:
        album_art_data['path'] = path
    if url is not None:
        album_art_data['url'] = url

    art_map[art_map_key] = album_art_data

def get_album_art_data_key(data):
    if 'album' in data and ('artist' in data or 'album_artist' in data):
        return '{artist} - {album_name}'.format(
            artist=data.get('album_artist', data['artist']),
            album_name=data['album']
        )
    else:
        return None

def set_album_cover_art(mp3_file, data, art_map=None):
    # Check for files on computer for song-specific cover art
    if 'song_art_path' in data:
        if apply_cover_art_from_file(mp3_file, data['song_art_path']):
            return

    # Check for URLs for song-specific cover art
    if 'song_art_url' in data:
        if apply_cover_art_from_url(mp3_file, data['song_art_url']):
            return

    # Check for files on computer for song-specific cover art
    if 'album_art_path' in data:
        if apply_cover_art_from_file(mp3_file, data['album_art_path']):
            add_album_art_data(art_map, data, path=data['album_art_path'])
            return

    # Check for URLs for song-specific cover art
    if 'album_art_url' in data:
        if apply_cover_art_from_url(mp3_file, data['album_art_url']):
            add_album_art_data(art_map, data, url=data['album_art_url'])
            return

    # Check map
    if art_map and get_album_art_data_key(data) is not None:
        apply_cover_art_from_map(mp3_file, data, art_map)

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

def yt_metadata():
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

    # Write album artwork data back to file
    if cover_art_map and cover_art_map_file:
        with open(cover_art_map_file, 'w') as f:
            json.dump(cover_art_map, f, indent=4)

# #################################################################################################
# Main method
# #################################################################################################

if __name__ == '__main__':
    try:
        # ==================================
        # Parse/validate args
        # ==================================
        args = sys.argv[1:]

        if len(args) < 2:
            error('wrong args; should be "<mp3-folder> <metadata-config> [<cover-art-config>]"')
            sys.exit(1)
        
        mp3_folder, metadata_file, *rest = args
        cover_art_file = rest[0] if len(rest) else None

        if not (
            os.path.isdir(mp3_folder) and 
            os.path.isfile(metadata_file) and
            (cover_art_file is None or os.path.isfile(cover_art_file))
        ):
            error('check that all paths are existing files/folders')
            sys.exit(1)

        no_write = False

        # ==================================
        # Read/validate metadata config data
        # ==================================
        try:
            with open(metadata_file) as f:
                metadata = json.load(f)
        except Exception as e:
            error('could not read metadata config')
            sys.exit(1)

        # Validate config (list of dicts)
        if not is_list(metadata) or not all([is_dict(d) for d in metadata]):
            error('metadata config is not well-formed')
            sys.exit(1)

        # ==================================
        # Read/validate album art config data
        # ==================================
        try:
            if cover_art_file:
                with open(cover_art_file) as f:
                    cover_art = json.load(f)
            else:
                cover_art = {}
        except Exception as e:
            error('could not read album art config')
            sys.exit(1)

        # Validate config (dict of dicts of dicts)
        if not is_dict(cover_art) or not all([
            (is_dict(d) and all([is_dict(v) for v in d])) 
            for d in cover_art
        ]):
            error('cover art config is not well-formed')
            sys.exit(1)
        
        # ==================================
        # Apply metadata
        # ==================================
        pass

        # ==================================
        # Write back to config files
        # ==================================
        if no_write:
            sys.exit(0)
        
        pass

    except Exception as e:
        error(e)
