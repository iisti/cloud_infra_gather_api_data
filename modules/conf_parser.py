#!/usr/bin/env python3

# For removing whitespaces
import re
# For parsing configuration file
# Set ExtendedInterpolation, check https://docs.python.org/3/library/configparser.html
from configparser import ConfigParser, ExtendedInterpolation

# logging
# https://stackoverflow.com/questions/13733552/logger-configuration-to-log-to-file-and-print-to-stdout
# https://www.loggly.com/ultimate-guide/python-logging-basics/
import logging

class ConfParser:
    """A class for parsing configuration files."""

    def __init__(self):
        self.config = ConfigParser(interpolation=ExtendedInterpolation())

    def load_ini_conf(self, conf_file):
        """Loads a configuration file.

        Parameters
        ----------
        config_file : str
            A configuration file in the OS with path.
        """

        self.config.read(conf_file)

    def get_logging_level(self):
        """Returns the log level which should be used for logging.
        logging.LEVEL's type is int."""

        log_level = self.config['Common']['log_level']
        if log_level.lower() == "debug":
            return logging.DEBUG
        elif log_level.lower() == "info":
            return logging.INFO
        elif log_level.lower() == "warning":
            return logging.WARNING
        elif log_level.lower() == "error":
            return logging.ERROR
        elif log_level.lower() == "critical":
            return logging.CRITICAL

    def get_log_path(self):
        """Return log path
        
        Returns
        -------
        str
            log output path.
        """

        return self.config['Common']['log_path']
    
    def print_conf(self):
        """Prints all data that was parsed from configuration file."""

        for each_section in self.config.sections():
            for (key, val) in self.config.items(each_section):
                if key == "access_token":
                    print(key, "=", "<CENSORED>")
                else:
                    print(key, "=", val)

    def get_conf_str(self):
        """Returns all data that was parsed from configuration file as
        a string."""

        # Temp variable for storing multiline string of configuration
        # parameters.
        tmp_conf = ""

        for each_section in self.config.sections():
            for (key, val) in self.config.items(each_section):
                # Create newline if something has been added already.
                if tmp_conf:
                    tmp_conf += "\n"
                tmp_conf += key + " = " + val

        return tmp_conf

    def get_output_path(self):
        """Return output path.
        
        Returns
        -------
        str
            log output path.
        """

        return self.config['Common']['output_path']
   
    def get_gcp_service_account_email(self):
        """Returns service account email."""
        
        return self.config['GCP']['service_account_email']

    def get_gcp_project_id(self):
        """Returns GCP Project ID string."""

        return self.config['GCP']['project_id']

    def get_gcp_zone(self):
        """Returns GCP zone."""

        return self.config['GCP']['zone']

    def get_gcp_credential_file(self):
        """Returns path to credential file."""

        return self.config['GCP']['credentials_file']

    def get_gcp_access_list(self):
        """Returns JSON of access information to GCP.
        
        Returns
        -------
        list
            Nested list with GCP access information.
        """
        
        access_str = self.config['GCP']['project_access_list']

        # Creating a nested list which items are lists with 4 values:
        # (project, zone, service account, credentials path)
        access_list = [item.split(',') for item in access_str.strip().split('\n')]

        return access_list
