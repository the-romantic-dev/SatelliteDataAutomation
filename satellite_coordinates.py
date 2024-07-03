import ephem
from datetime import datetime

from util import SatelliteType


def get_tle_filename(satellite_type: SatelliteType):
    match satellite_type:
        case SatelliteType.AQUA:
            return "AQUA_TLE.txt"
        case SatelliteType.ELEKTRO_L3:
            return "ELEKTRO_L3_TLE.txt"
        case SatelliteType.SUOMI_NPP:
            return "SUOMI_NPP_TLE.txt"
        case _:
            raise ValueError("Неизвестный тип спутника")


def refactor_cord_for_filename(cord):
    sp = cord.split(":")
    return f"{sp[0]}°{sp[1]}\'{sp[2]}\'\'"


def get_coordinates(satellite_type: SatelliteType, date_obj: datetime):
    tle_folder = "tle"
    tle_filepath = f"{tle_folder}\\{get_tle_filename(satellite_type)}"

    with open(tle_filepath, 'r') as file:
        tle_lines = [line for line in file]

    name = tle_lines[0]
    line1 = tle_lines[1]
    line2 = tle_lines[2]

    iss = ephem.readtle(name, line1, line2)

    date_str = date_obj.strftime("%Y/%m/%d %H:%M:%S:%f")
    iss.compute(date_str)
    long = str(iss.sublong)
    lat = str(iss.sublat)
    return refactor_cord_for_filename(long), refactor_cord_for_filename(lat), iss.elevation
