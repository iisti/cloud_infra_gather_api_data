# gcp_gather_api_data
A project for gathering relevant data from GCP API about VMs/etc in GCP.

## Development instructions
### On Windows 10
1. Install WSL (Windows Subsystem Linux (the easiest way to use Linux in Windows)

### Installing Python3 and virtualenv on Debian WSL
1. Clone the repository

       git clone https://github.com/iisti/gcp_gather_api_data.git
1. Install Python3 and pip3

       sudo apt-get install python3 python3-pip
1. Install virtualenv using pip3

       pip3 install virtualenv
1. Create virtual environment

       virtualenv gcp_gather_api_data/virtualenv
1. Activate virtual environment

       source gcp_gather_api_data/virtualenv/bin/activate
1. One can check which virtualenv is in use by:

       echo $VIRTUAL_ENV
       /home/iisti/scripts/gcp_gather_api_data/virtualenv
1. Deactivate (just to know how it's done)

       deactivate

1. Install modules

        # Remember to activate virtualenv before
        pip3 install -r requirements.txt

1. Create service account for connecting to GCP API. Follow instructions from:
  * Source: https://libcloud.readthedocs.io/en/stable/compute/drivers/gce.htm
  1. GCP Projcet -> IAM & Admin -> Service Accounts -> Create service account
  1. Input name.
  1. Step: Grant this service account access to project (optional)
    * User role "Basic: viewer" = Read access to all resources.
  1. Step: Grant users access to this service account (optional)
    * This is not needed.
  1. Select the new service account and create new key in JSON format.
  1. Copy/move the credential JSON to this project root and rename it with prefix "credential_", so
     that the credentials will not be uploaded to GitHub by accident.
