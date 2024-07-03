import os
from datetime import datetime
from enum import Enum


class SatelliteType(Enum):
    AQUA = 0
    ELEKTRO_L3 = 1
    SUOMI_NPP = 2


def get_pipeline_by_satellite_type(satellite_type: SatelliteType):
    match satellite_type:
        case SatelliteType.AQUA:
            return "aqua_db"
        case SatelliteType.ELEKTRO_L3:
            return "elektro_rdas"
        case SatelliteType.SUOMI_NPP:
            return "npp_hrd"
        case _:
            raise ValueError("Неизвестный тип спутника")


def get_satellite_type_by_data_subdir(data_folder):
    match data_folder.lower():
        case 'aqua':
            return SatelliteType.AQUA
        case 'elektro-l3':
            return SatelliteType.ELEKTRO_L3
        case 'suomi npp':
            return SatelliteType.SUOMI_NPP
        case _:
            raise ValueError("Неизвестный тип спутника")


def count_files(directory):
    total_files = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if 'processed' not in file:
                total_files += 1

    return total_files


def filename_to_date(name):
    _, date_str, time_str = name.split('.')[0].split("_")
    date_obj = datetime.strptime(f"{date_str}{time_str}", "%d%m%y%H%M%S")
    return date_obj


def timestamp_to_date(timestamp):
    date_obj = datetime.fromtimestamp(timestamp)
    return date_obj


def create_dir(path):
    try:
        os.mkdir(path)
        print(f"Directory created successfully")
    except Exception as e:
        print(f"Failed to create directory : {e}")
