import json
import os
import subprocess
import time

from satellite_coordinates import get_coordinates
from util import SatelliteType, get_pipeline_by_satellite_type, count_files, get_satellite_type_by_data_subdir, \
    filename_to_date, timestamp_to_date, create_dir
from dataclasses import dataclass

# Дефолтное название папки вывода до полного декодирования, после которого она переименовывается
DEFAULT_FOLDER = "last_data"
# Строка, добавляющаяся в конец названия декодированного файла
PROCESSED_FLAG = "processed"


@dataclass
class DecodingArgs:
    """Date class for storing arguments passed to the decoder"""
    exe_path: str
    satellite_type: SatelliteType
    data_subdir: str
    input_filename: str
    output_subdir: str


def run_decoder(args: DecodingArgs):
    """Decodes a single file using satdump.exe located in the Satdump installation folder on the exe_path path"""

    pipeline_id = get_pipeline_by_satellite_type(args.satellite_type)
    command = (f'\"{args.exe_path}\" {pipeline_id} cadu '
               f'\"{args.data_subdir}\\{args.input_filename}\" \"{args.output_subdir}\\{DEFAULT_FOLDER}\"')

    print(f'Decoding a file {args.input_filename}')
    start_time = time.time()
    subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
    end_time = time.time()
    print(f'File {args.input_filename} successfully decoded to a folder {args.output_subdir}')
    print(f"Decoding time: {end_time - start_time} seconds")


def decode_all(exe_path, data_dir, output_dir, progress_var, callback):
    """Decodes all files in the data_dir folder sequentially using run_decoder()"""

    data_folders = os.listdir(data_dir)
    files_total_count = count_files(data_dir)
    print(f"Total data files: {files_total_count}")
    if files_total_count == 0:
        callback()
        print("There are no files to decode")
        return

    tick = 1000 / files_total_count

    for subdir in data_folders:
        satellite_type = get_satellite_type_by_data_subdir(subdir)
        data_subdir = f'{data_dir}\\{subdir}'
        data_files = os.listdir(data_subdir)
        output_subdir = f'{output_dir}\\{subdir}'
        if not os.path.exists(output_subdir):
            create_dir(output_subdir)

        for name in data_files:
            if PROCESSED_FLAG not in name:
                args = DecodingArgs(
                    exe_path=exe_path,
                    satellite_type=satellite_type,
                    data_subdir=data_subdir,
                    input_filename=name,
                    output_subdir=output_subdir)

                run_decoder(args)
                progress_var.set(progress_var.get() + tick)

                os.rename(f'{data_subdir}\\{name}',
                          f'{data_subdir}\\{name.split(".")[0]}_{PROCESSED_FLAG}.{name.split(".")[1]}')

                rename_output_subdir(args)
    callback()


def rename_output_subdir(args: DecodingArgs):
    """Renames the folder with the decoding result, making up the name from the date and position of the satellite"""
    if args.satellite_type == SatelliteType.ELEKTRO_L3:
        date_obj = filename_to_date(args.input_filename)
    else:
        data_timestamp = get_timestamp(args.output_subdir)
        date_obj = timestamp_to_date(data_timestamp)
    date_str = date_obj.strftime("%d.%m.%Y %Hh%Mm%Ss")
    cords = get_coordinates(satellite_type=args.satellite_type, date_obj=date_obj)
    os.rename(f'{args.output_subdir}\\{DEFAULT_FOLDER}',
              f'{args.output_subdir}\\{date_str} long {cords[0]} lat {cords[1]} elev {cords[2]}m')


def get_timestamp(target_folder):
    path = f"{target_folder}\\{DEFAULT_FOLDER}\\dataset.json"
    if os.path.exists(path):
        with open(path, 'r') as f:
            json_data = json.load(f)
            return json_data["timestamp"]
    else:
        return None
