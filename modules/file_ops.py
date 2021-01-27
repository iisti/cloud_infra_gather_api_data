#!/usr/bin/env python3

# For logging into file
import logging

# JSON handling
import json

# CSV handling
import csv

# Time stamps to files
from datetime import datetime

# For checking instance type of GCENodeDriver
#from libcloud.compute.types import Provider
#from libcloud.compute.providers import get_driver
from libcloud.compute.drivers.gce import GCENodeDriver

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
    if not output_path:
        logging.error("Func: {} no output_path given.".format(inspect.stack()[0][3]))
        return

    file_out = output_path + file_name + "_" + \
            datetime.now().strftime("%Y%m%d-%H%M%S") + \
            ".json"
    logging.info("Writing JSON: " + file_out)
    with open(file_out, 'w') as outfile:
        json.dump(json_obj, outfile, indent=4, ensure_ascii=False)

    return file_out

def write_csv_nodes(node_list: list = None,
        file_name: str = None,
        output_path: str = None):
    
    if not node_list:
        logging.error("Func: {} no node_list given.".format(inspect.stack()[0][3]))
        return
    if not file_name:
        logging.warning("Func: {} no file_name given.".format(inspect.stack()[0][3]))
        file_name = "no_name_given"
    if not output_path:
        logging.error("Func: {} no output_path given.".format(inspect.stack()[0][3]))
        return

    file_out = output_path + file_name + "_" + \
            datetime.now().strftime("%Y%m%d-%H%M%S") + \
            ".csv"
    
    logging.info("Writing text dump of list: " + file_out)
    
    #with open(file_out, 'w') as outfile:
    #    for item in node_list:
    #        print(item.id, item.name, item.state)
    #        outfile.write(item.id + item.name + item.size) 

    with open(file_out, mode='w') as outfile:
        node_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        node_writer.writerow([
            'Provider',
            'Project',
            'Zone',
            'VM Name',
            'Public IPs',
            'Private IPs',
            'State',
            'Size',
            'Image',
            'ID'])

        for node in node_list:
            if isinstance(node.driver, GCENodeDriver):
                provider = "GCP"
                project = node.driver.project
                zone = node.driver.zone.name
                separator = ';'
                public_ips = convert_list_to_str(node.public_ips, separator)
                private_ips = convert_list_to_str(node.private_ips, separator)
            node_writer.writerow([
                provider,
                project,
                zone,
                node.name,
                public_ips,
                private_ips,
                node.state,
                node.size,
                node.image,
                node.id])
    
    # Return the file path str
    return file_out

def convert_list_to_str(list_obj: list = None, separator: str = None):
    if not list_obj:
        logging.error("Func: {} no list_obj given.".format(inspect.stack()[0][3]))
        return
    if not separator:
        logging.error("Func: {} no separator given.".format(inspect.stack()[0][3]))
        return
    
    tmp_str = ""
    for item in list_obj:
        if tmp_str:
            tmp_str += separator
        if item is None:
            tmp_str += "None"
        else:
            tmp_str += item

    return tmp_str

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
