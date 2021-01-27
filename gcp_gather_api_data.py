#!/usr/bin/env python3

"""GCP Gather API Data

This is a program for gathering data from GCP API for IT adminstration purposes.


Usage:
    gcp_gather_api_data.py (-c <FILE> | --config <FILE>)
    gcp_gather_api_data.py (-h | --help)
    gcp_gather_api_data.py --version

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

def retrieve_node_list(conf: ConfParser = None, driver: Provider = None):
    if conf == None or not isinstance(conf, ConfParser):
        logging.error("Func: {} no conf given.".format(inspect.stack()[0][3]))
        return
    
    if driver == None or not isinstance(driver, Provider):
        logging.error("Func: {} no Libcloud driver given.".format(inspect.stack()[0][3]))
        return
    




def main():
    arguments = docopt(__doc__, version='GCP Gather API Data 0.1')
    config = ConfParser()
    config.load_ini_conf(arguments["--config"])

    # Create log file
    log_to_file(config, "gcp_gather_api_data")

    # Print loaded configuration
    logging.info("Loaded configuration:\n" + config.get_conf_str())

    gcp_access_id = config.get_gcp_service_account_email()
    # File can be either JSON or P12 format
    gcp_credential_file = config.get_gcp_credential_file()
    gcp_project_id = config.get_gcp_project_id()
    gcp_zone = config.get_gcp_zone()
   
    gcp_driver = get_driver(Provider.GCE)

    drivers = [gcp_driver(gcp_access_id,
            gcp_credential_file,
            project=gcp_project_id,
            datacenter=gcp_zone)]

    nodes = []
    for driver in drivers:
        nodes += driver.list_nodes()
    
    print(nodes)
    # Write a JSON file of the instences/nodes
    #file_ops.write_json_dump(nodes, "gcp_braintribe-anexia-vms", config.get_output_path())

# Example:
# https://realpython.com/python-logging/
def log_to_file(config: ConfParser = None, log_id: str = None):
    log_path = config.get_log_path()
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
