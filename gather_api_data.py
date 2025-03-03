#!/usr/bin/env python3

"""GCP Gather API Data

This is a program for gathering data from GCP API for IT adminstration purposes.


Usage:
    gather_api_data.py (-c <FILE> | --config <FILE>)
    gather_api_data.py (-h | --help)
    gather_api_data.py --version

Options:
    -h --help   Show this screen.
    --version   Show version.
    -c --config Configuration file.

"""

# -*- coding: utf-8 -*-
# For documentation
from docopt import docopt

# For logging
# https://stackoverflow.com/questions/13733552/logger-configuration-to-log-to-file-and-print-to-stdout
# https://www.loggly.com/ultimate-guide/python-logging-basics/
import logging
import logging.handlers
import os
# Retrieve the name of current function
import inspect

# JSON handling
import json

# CSV and JSON file operations and printing
import modules.file_ops as file_ops

# CSV handling
import csv

# Time stamps to files
from datetime import datetime

# For creating requests to GitHub API
import requests

# For parsing configurations
from modules.conf_parser import ConfParser

# Apache Libcloud, for retrieving stuff from cloud providors.
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

# For retriving path where the gather_api_data.py resides, so that the files
# can be written relatively to it.
import os

# For checking instance type of GCENodeDriver
#from libcloud.compute.drivers.gce import GCENodeDriver

#def retrieve_node_list(conf: ConfParser = None):
#    if conf == None or not isinstance(conf, ConfParser):
#        logging.error("Func: {} no conf given.".format(inspect.stack()[0][3]))
#        return
#    
#    gcp_access_id = conf.get_gcp_service_account_email()
#    # File can be either JSON or P12 format
#    gcp_credential_file = conf.get_gcp_credential_file()
#    gcp_project_id = conf.get_gcp_project_id()
#    gcp_zone = conf.get_gcp_zone()
#   
#    gcp_driver = get_driver(Provider.GCE)
#
#    drivers = [gcp_driver(gcp_access_id,
#            gcp_credential_file,
#            project=gcp_project_id,
#            datacenter=gcp_zone)]
#
#    nodes = []
#    for driver in drivers:
#        nodes += driver.list_nodes()
#
#    return nodes

def retrieve_node_list2(conf: ConfParser = None, access_list: list = None):
    if conf == None or not isinstance(conf, ConfParser):
        logging.error("Func: {} no conf given.".format(inspect.stack()[0][3]))
        return
    
    #gcp_access_id = conf.get_gcp_service_account_email()
    ### File can be either JSON or P12 format
    #gcp_credential_file = conf.get_gcp_credential_file()
    #gcp_project_id = conf.get_gcp_project_id()
    #gcp_zone = conf.get_gcp_zone()
   
    gcp_driver = get_driver(Provider.GCE)

    drivers = list()

    base_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
    
    # Order of items in the nested acccess_list:
    # [[project, zone, service account, credential file], [etc...]]
    for access in access_list:
        # driver needs args in order access_id, credential_file, project, datacenter/zone
        drivers.append(gcp_driver(access[2], base_dir + access[3], project=access[0], datacenter=access[1]))

    #drivers = [gcp_driver(gcp_access_id,
    #        gcp_credential_file,
    #        project=gcp_project_id,
    #        datacenter=gcp_zone)]

    nodes = []
    for driver in drivers:
        nodes += driver.list_nodes()

    return nodes

def main():
    arguments = docopt(__doc__, version='GCP Gather API Data 0.1')
    config = ConfParser()
    config.load_ini_conf(arguments["--config"])

    # Create log file
    log_to_file(config, "gather_api_data")

    # Print loaded configuration
    logging.info("Loaded configuration:\n" + config.get_conf_str())

    access_list = config.get_gcp_access_list()

    #for items in access_list:
    #    for item in items:
    #        print(item, end = ' ')

    #nodes = retrieve_node_list(config)
    nodes = retrieve_node_list2(config, access_list)
    
    base_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
    
    file_ops.write_csv_nodes(nodes, "vms", base_dir + config.get_output_path())
   

    # Not needed
    # Write a JSON file of the instences/nodes
    #file_ops.write_json_dump(nodes, "gcp_braintribe-anexia-vms", config.get_output_path())

# Example:
# https://realpython.com/python-logging/
def log_to_file(config: ConfParser = None, log_id: str = None):
    base_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
    log_path = base_dir + config.get_log_path()
    log_name = log_path + log_id + "_" + \
            datetime.now().strftime("%Y%m%d-%H%M%S") + ".log"

    # Probably some import initializes the logging already,
    # but logging needs to be initialized this way to get the
    # output to certain file.
    # https://stackoverflow.com/a/46098711
    logging.root.handlers = []
    logging.basicConfig(level=config.get_logging_level(), \
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_name),
                logging.StreamHandler()
            ]
    )

if __name__ == '__main__':
    main()
