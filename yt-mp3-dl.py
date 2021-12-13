import sys
import os
import subprocess

# #################################################################################################
# Logging helpers
# #################################################################################################

def divider():
    print('===============================================================')

def log(s):
    print('[YT-MP3-DL][LOG]   : {}'.format(s))

def error(s):
    print('[YT-MP3-DL][ERROR] : {}'.format(s))

# #################################################################################################
# Command-line helpers
# #################################################################################################

'''
    Runs command-line program
    Takes in a list of args
    Will raise an exception if the command fails
'''
def run_cmd(cmd):
    proc_result = subprocess.run(
        cmd, 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )

    if proc_result.returncode:
        raise Exception(f'command ({cmd}) returned non-zero code')

'''
    Runs youtube-dl utility to download YouTube video as M4A at url to path
    Note that YouTube usually doesn't offer MP3 audio downloads, 
    necessitating an intermediate conversion from M4A
'''
def dl_m4a(path, url):
    run_cmd(['youtube-dl', '-o', path, '-f' '140', url])

'''
    Runs ffmpeg utility to convert M4A m4a_path to MP3 mp3_path
'''
def convert_m4a_to_mp3(m4a_path, mp3_path):
    run_cmd(['ffmpeg', '-i', m4a_path, '-acodec', 'libmp3lame', '-aq', '2', mp3_path])

# #################################################################################################
# download_yt
# #################################################################################################

'''
    Parse well-formatted line into URL and filename
    Returns tuple (url, filename)
    Raises exception if line cannot be parsed
'''
def parse_url_filename_pair(line):
    url, _, filename = line.partition(' | ')

    if not (url and filename):
        raise Exception('line cannot be parsed')
        
    return url.strip(), filename.strip()

def construct_file_path(folder, name, ext):
    os.path.join(folder, '{name}.{ext}'.format(name, ext))

'''
    Downloads a YouTube video at url as MP3
    Stores in dest_folder under filename.mp3
    If lazy is true, will not overwrite M4A/MP3 files
    If clean is true, will clean M4A download files
    Returns a list of log messages
'''
def _download_yt(
    url, 
    dest_folder, 
    filename, 
    lazy=False, 
    clean=True
):
    logs = []

    # Construct filenames
    m4a_path = construct_file_path(dest_folder, filename, '.m4a')
    mp3_path = construct_file_path(dest_folder, filename, '.mp3')

    return logs

'''
    Downloads a YouTube video at url as MP3
    Stores in dest_folder under filename.mp3
    If lazy is true, will not overwrite M4A/MP3 files
    If clean is true, will clean M4A download files
    Returns a list of log messages
'''
def download_yt(url, dest_folder, filename, lazy=False, clean=True):
    # Buffer logs
    logs = []

    # Construct filenames
    m4a_path = os.path.join(dest_folder, '{name}.m4a'.format(name=filename))
    mp3_path = os.path.join(dest_folder, '{name}.mp3'.format(name=filename))

    # Check if MP3 already exists
    # Depending on lazy flag, skip or delete
    if os.path.isfile(mp3_path):
        if lazy:
            logs.append(['"{}" MP3 already exists; skipping'.format(filename)])
            return logs
        # Remove the existing file
        os.remove(mp3_path)
        logs.append('"{}" MP3 already exists; deleting'.format(filename))
    
    # Check if M4A download already exists
    # Depending on lazy flag, re-download or delete
    if os.path.isfile(m4a_path):
        if lazy:
            logs.append('"{}" M4A already exists; skipping download'.format(filename))
        else:
            os.remove(m4a_path)
            logs.append('"{}" M4A already exists; deleting'.format(filename))
            # Download M4A
            dl_m4a(m4a_path, url)
            logs.append('downloading M4A "{}"'.format(url, filename))
    else:
        # Download M4A
        dl_m4a(m4a_path, url)
        logs.append('downloading M4A "{}"'.format(url, filename))

    # Convert M4A to MP3
    convert_m4a_to_mp3(m4a_path, mp3_path)
    logs.append('converting M4A to MP3 "{}"'.format(filename))

    # Clean up M4A
    if clean:
        os.remove(m4a_path)
    
    return logs

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
            error('wrong args; should be "<input-file> <dest-folder> [--lazy] [--no-clean]"')
            sys.exit(1)        
        input_file, dest_folder, *flags = args
        if not (os.path.isfile(input_file) and os.path.isdir(dest_folder)):
            error('check that both input file and destination folder exist')
            sys.exit(1)
        # Flags: --lazy, --no-clean
        lazy = '--lazy' in flags
        clean = '--no-clean' not in flags

        # ==================================
        # Parse URL file
        # ==================================
        try:
            with open(input_file) as f:
                url_filename_pairs = [parse_url_filename_pair(l) for l in f.readlines()]
        except Exception as e:
            error('could not parse file "{}"; check README for format'.format(urls_and_filenames))
            sys.exit(1)

        # ==================================
        # Download MP3s
        # ==================================
        for url, filename in url_filename_pairs:
            try:
                msgs = download_yt(url, dest_folder, filename, lazy=lazy, clean=clean)
                divider()
                for msg in msgs: log(msg)
            except Exception as e:
                divider()
                error('could not download "{filename}" ({url}): {e}'.format(filename=filename, url=url, e=str(e)))
        divider() if len(url_filename_pairs) else None
    except Exception as e:
        error(e)
