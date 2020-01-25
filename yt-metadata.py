#
# Script for batch modifying MP3 file metadata using JSON configs
# Make sure that you "pip install -r requirements.txt" before running this script, as it relies
# on third-party libraries (i.e. eyeD3)
#


import sys
import json
import os

import eyed3


def apply_metadata_tag(mp3_file, tag_name, data, fallback_tag_name=None):
    tag_value = data.get(tag_name, data.get(fallback_tag_name) if fallback_tag_name else None)

    if not tag_value:
        return

    setattr(mp3_file.tag, tag_name, tag_value)


def apply_mp3_metadata(data, folder):
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

    mp3_file.tag.save()


if __name__ == '__main__':
    # Check arguments
    if len(sys.argv) != 3:
        print('Too many/few arguments; pass in a MP3 file folder and JSON config path to this script')
        sys.exit(2)

    mp3_folder = sys.argv[1]
    json_config = sys.argv[2]

    # Check that folder and file exist
    if not os.path.isfile(json_config) or not os.path.isdir(mp3_folder):
        print('Either {dir} is not an existing directory or {file} is not an existing file'.format(
            dir=mp3_folder, file=json_config
        ))
        sys.exit(1)

    # Parse JSON
    # This file will contain all the metadata you'd like to apply to your MP3 files
    try:
        with open(json_config) as f:
            mp3_metadata = json.load(f)
    except Exception as e:
        print('Could not load JSON config: {error}'.format(error=str(e)))
        sys.exit(1)

    # Check shape of data
    if not isinstance(mp3_metadata, list):
        print('Your MP3 metadata JSON object should be a list of properly formatted objects, see README.md for details')
        sys.exit(1)

    # Iterate through metadata object and apply metadata to MP3 file
    successes = failures = 0

    for metadata in mp3_metadata:
        try:
            apply_mp3_metadata(metadata, mp3_folder)
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
