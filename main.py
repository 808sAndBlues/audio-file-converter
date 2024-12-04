import argparse
import glob
import os

from pydub import AudioSegment

"""
TODO:

    Add command line argument for:
        - folder
        - output format
    
    Search through folder for .flac files
    Output files to selected output format with shrunken names
"""

DEFAULT_ALBUM_NAME: str = 'None'
DEFAULT_ARTIST_NAME: str = 'None'
DEFAULT_INPUT_FORMAT: str = 'mp3'
DEFAULT_OUTPUT_FORMAT: str = 'mp3'
DEFAULT_OUTPUT_RATE: str = '256k'
DEFAULT_SOURCE_FILE_PATH: str = 'None'

CONVERTED_FILE_DIR: str = '/CONVERTED/'

ARGUMENTS = [('--album', str, DEFAULT_ALBUM_NAME, 'Album name', '?'),
             ('--artist', str, DEFAULT_ARTIST_NAME, 'Artist name', '*'),
             ('--output-format', str, DEFAULT_OUTPUT_FORMAT, 'Output format',
              '?'),
             ('--source-file-path', str, DEFAULT_SOURCE_FILE_PATH,
              'Default source file path', '?'),
             ('--output-rate', str, DEFAULT_OUTPUT_RATE,
              'Default output rate', '?'),
             ('--input-format', str, DEFAULT_INPUT_FORMAT, 'Input format', '?')]


def create_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog= "AudioConverter",
                                     usage= "Convert audio clips to various "
                                             "formats")
    
    for argument in ARGUMENTS:
        parser.add_argument(argument[0], type=argument[1], default=argument[2],
                            help=argument[3], nargs=argument[4])

    return parser


def retrieve_files(folder_path: str, original_file_format: str):
    updated_path: str = folder_path + "/*." + original_file_format
    return glob.glob(updated_path)


def retrieve_filename_no_extension(file_name, input_format: str) -> str:
    space_split = file_name.split()

    # Skip first element as that is the raw file path leading up to name
    title: str = ' '.join(space_split[1:])
    
    # Need to remove file extension from path
    file_name_delimiter: str = "." + input_format
    arr = title.split(file_name_delimiter)
    
    return arr[0]


def create_converted_dir(new_dir_path: str):
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)

def generated_converted_dir_str(source_file_path: str) -> str:
    return source_file_path + CONVERTED_FILE_DIR


def convert_files(retrieved_files, input_format: str, output_format: str,
                  bit_rate: str, album: str, artist: str, holding_dir: str):
    built_tags = None

    if output_format == 'mp3':
        built_tags = {"album": album, "artist": artist}

    for file in retrieved_files:
        new_file = (holding_dir +
                    retrieve_filename_no_extension(file, input_format) + '.' +
                    output_format)

        print("Creating: ", new_file)
        

        
        try:
            sound = AudioSegment.from_file(file, format=input_format,
                                       bitrate=bit_rate,
                                       tags=built_tags)

            sound.export(new_file, format=output_format, bitrate=bit_rate,
                         tags=built_tags)
            
        except Exception as err:
            print(err)


def update_args(args: dict) -> None:
    artist: str = args['artist'][0]

    for i in range(1, len(args['artist'])):
        artist += ' ' + args['artist'][i]
    
    args['artist'] = artist


if __name__ == "__main__":
    parser: argparse.ArgumentParser = create_arg_parser()
    passed_args: dict = vars(parser.parse_args())

    update_args(passed_args)

    converted_dir_path = generated_converted_dir_str(
            passed_args['source_file_path'])

    create_converted_dir(converted_dir_path)

    files = retrieve_files(passed_args['source_file_path'],
                           passed_args['input_format'])

    convert_files(files, passed_args['input_format'],
                  passed_args['output_format'],
                  passed_args['output_rate'],
                  passed_args['album'],
                  passed_args['artist'],
                  converted_dir_path)

