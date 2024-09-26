# SeeYou documentation:
#    https://downloads.naviter.com/docs/SeeYou_CUP_file_format.pdf
# Little Navmap documentation:
#    https://www.littlenavmap.org/manuals/littlenavmap/release/3.0/en/USERPOINT.html#types
import logging
import argparse
import os
import csv


def main(args):
    """First it is checked wether the supplied file exists. Then the file is read.
    Before it is closed, it is parsed and written to a new csv file.
    """
    for cup_file in args.cupfiles:
        cup_file_abspath = os.path.abspath(cup_file)

        if not os.path.isfile(cup_file_abspath):
            log.error('File does not exist.')
            exit()

        with open(cup_file_abspath, 'r', newline='') as file_cup:
            log.info(f'Reading file   : \"{cup_file_abspath}\"')
            reader = csv.DictReader(file_cup)

            with open(new_extension(cup_file_abspath, 'csv'), 'w', newline='') as file_csv:
                log.info(f'Writing to file: \"{new_extension(cup_file_abspath, "csv")}\"')
                writer = csv.DictWriter(file_csv, fieldnames=get_field_keys())
                writer.writeheader()

                for cup_row in reader:
                    writer.writerow(create_user_point(cup_row))
    log.info('Task completed.')


def new_extension(path, ext):
    return os.path.abspath(f'{path}.{ext}')


def get_field_keys():
    """return: List of LNM fieldnames.
    """
    return [
        'Type',
        'Name',
        'Ident',
        'Latitude',
        'Longitude',
        'Elevation',
        'Magnetic Declination',
        'Tags',
        'Description',
        'Region',
        'Visible From'
    ]


def create_user_point(cup_row):
    """return: Dictionary with single userpoint data as per the LNM fieldnames.
    """
    values = [
        get_type(cup_row),
        get_name(cup_row),
        get_ident(cup_row),
        get_latitude(cup_row),
        get_longitude(cup_row),
        get_elevation(cup_row),
        get_magnetic_declination(cup_row),
        get_tags(cup_row),
        get_description(cup_row),
        get_region(cup_row),
        get_visible_from(cup_row)
    ]
    return {field_keys: values for field_keys, values in zip(get_field_keys(), values)}


def get_type(cup_row):
    """Use CUP-style to LNM-type mapping with `Unknown` as fallback.
    return: String of LNM-compatible type.
    """
    types = list(cup_style_mapping().values())
    return types[int(cup_row.get('style', '0'))]


def get_name(cup_row):
    """return: String with userpoint name if applicable else None.
    """
    return cup_row.get('name', None)


def get_ident(cup_row):
    """return: String with userpoint code if applicable else None.
    """
    return cup_row.get('code', None)


def get_latitude(cup_row):
    """SeeYou Cup format is [deg0, deg1, min0, min1, ., mdl0, mdl1, mdl2, N/S].
    return: float of latitude in decimal format.
    """
    degrees     = int(cup_row["lat"][:2])
    minutes     = float(cup_row["lat"][2:-1])
    north_south = {"N": 1, "S": -1}[cup_row["lat"][-1].upper()]
    return north_south * (degrees + minutes / 60)


def get_longitude(cup_row):
    """SeeYou Cup format is [deg0, deg1, deg2, min0, min1, ., mdl0, mdl1, mdl2, E/W].
    return: float of longitude in decimal format.
    """
    degrees   = int(cup_row["lon"][:3])
    minutes   = float(cup_row["lon"][3:-1])
    east_west = {"E": 1, "W": -1}[cup_row["lon"][-1].upper()]
    return east_west * (degrees + minutes / 60)


def get_elevation(cup_row):
    """return: String of elevation with m or f as suffix for meters or feet if applicable else None.
    """
    if cup_row.get('elev', None):
        return cup_row["elev"].replace('ft', 'f')
    else:
        return None


def get_magnetic_declination(cup_row):
    """Not in CUP format.
    return: None.
    """
    return None


def get_tags(cup_row):
    """No use.
    return: None.
    """
    return None


def get_description(cup_row):
    """Create description containing data from fields in the CUP format otherwise not supported by LNM.
    return: String of extra information not specified in other fields.
    """
    styles = list(cup_style_mapping().keys())
    desc   = ''
    if cup_row.get('desc', None):
        desc += cup_row["desc"]
    if cup_row.get('style', None):
        desc += f' | {styles[int(cup_row["style"])]}'
    if cup_row.get('rwdir', None):
        desc += f' | rwdir: {cup_row["rwdir"]}'
    if cup_row.get('rwlen', None):
        desc += f' | rwlen: {cup_row["rwlen"]}'
    if cup_row.get('freq', None):
        desc += f' | freq: {cup_row["freq"]}'
    if cup_row.get('userdata', None):
        desc += f' | userdata: {cup_row["userdata"]}'
    return desc


def get_region(cup_row):
    """Not implemented.
    return: None.
    """
    return None


def get_visible_from(cup_row):
    """Not in CUP format.
    return: None.
    """
    return None


def cup_style_mapping():
    """Maps the CUP-format styles to LMN-compatible types.
    See SeeYou & Little Navmap documentations.
    return: Dictionary of mapping.
    """
    return {
        "Unknown"                           : "Unknown",
        "Waypoint"                          : "Waypoint",
        "Airfield with grass surface runway": "Airport",
        "Outlanding"                        : "Location",
        "Gliding airfield"                  : "Airstrip",
        "Airfield with solid surface runway": "Airport",
        "Mountain Pass"                     : "Mountain",
        "Mountain Top"                      : "Mountain",
        "Transmitter Mast"                  : "Obstacle",
        "VOR"                               : "VOR",
        "NDB"                               : "NDB",
        "Cooling Tower"                     : "POI",
        "Dam"                               : "POI",
        "Tunnel"                            : "POI",
        "Bridge"                            : "POI",
        "Power Plant"                       : "POI",
        "Castle"                            : "POI",
        "Intersection"                      : "POI",
        "Marker"                            : "Marker",
        "Control/Reporting Point"           : "VRP",
        "PG Take Off"                       : "Obstacle",
        "PG Landing Zone"                   : "Obstacle"
    }


def get_clas(arg=None):
    """return: Argparse class.
    """
    desc   = 'Little NavCup: Convert CUP Waypoints to CSV Userpoints for Little Navmap.'
    parser = argparse.ArgumentParser(prog='main.py', description=desc, epilog='')
    parser.add_argument('cupfiles', type=str, nargs='+', help='str: Paths to CUP files. Multiple paths can be supplied.')
    return parser.parse_args(arg)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]: %(message)s')
    log = logging.getLogger(__name__)
    try:
        args = get_clas()
        main(args)
    except Exception as e:
        log.exception(e)
