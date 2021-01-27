#!/usr/bin/env python3

# For logging into file
import logging

# JSON handling
import json

# CSV handling
import csv

# Time stamps to files
from datetime import datetime

def open_json(file_name: str = None):
    """Opens a JSON file.
    Parameters
    ----------
    str
        To be opened file with path.
    """

    if not file_name:
        logging.error("Func: {} no file_name given.".format(inspect.stack()[0][3]))
        return

    logging.debug("Opening JSON file: " + file_name)
    json_file = ""
    try:
        with open(file_name, 'r') as f:
            json_file = json.load(f)
    except (IOError, IsADirectoryError) as e:
        logging.error(e)

    return json_file

def get_json_dump(json_obj):
    """Function for creating prettyPrint JSON."""

    if not json_obj:
        logging.error("Func: {} no JSON obj given.".format(inspect.stack()[0][3]))
        return

    return json.dumps(json_obj, indent=4, ensure_ascii=False)

def print_json_dump(json_obj: list = None):
    """Function mainly for test console prints"""

    if not json_obj:
        logging.error("Func: {} no JSON obj given.".format(inspect.stack()[0][3]))
        return
    
    print(json.dumps(json_obj, indent=4, ensure_ascii=False))

def write_json_dump(json_obj: list = None,
        file_name: str = None,
        output_path: str = None):
    """Writes JSON dump to given folder.

    Parameters
    ----------


    Returns
    -------
    str
        Output dir + filename
    """

    if not json_obj:
        logging.error("Func: {} no JSON obj given.".format(inspect.stack()[0][3]))
        return
    if not file_name:
        logging.warning("Func: {} no file_name given.".format(inspect.stack()[0][3]))
        file_name = "no_name_given"

    file_out = output_path + file_name + "_" + \
            datetime.now().strftime("%Y%m%d-%H%M%S") + \
            ".json"
    logging.info("Writing JSON: " + file_out)
    with open(file_out, 'w') as outfile:
        json.dump(json_obj, outfile, indent=4, ensure_ascii=False)

    return file_out

# NEEDS WORK
def write_csv(json_dict: dict = None,
        file_name: str = None,
        output_path: str = None):
    """Writes GitHub login names and real names into CSV file."""

    file_out = output_path + file_name + "_" + \
            datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv"

    logging.info("Writing CSV: " + file_out)

    with open(file_out, mode='w') as outfile:
        name_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        name_writer.writerow(['GitHub login', 'Name'])

        for user, real_name in json_dict.items():
            name_writer.writerow([user, real_name])
