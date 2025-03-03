# Cloud Infrastructure Gather API Data
* A project for gathering relevant data from cloud providers API about VMs/etc.
  * Relevant data means: what is running where and IPs/etc.

## Development instructions
### On Windows 10
1. Install WSL (Windows Subsystem Linux (the easiest way to use Linux in Windows)

### Installing Python3 and virtualenv on Debian WSL
1. Clone the repository

       git clone https://github.com/iisti/cloud_infra_gather_api_data.git
1. Install Python3 and pip3

       sudo apt-get install python3 python3-pip
1. Install virtualenv using pip3

       pip3 install virtualenv
1. Create virtual environment

       virtualenv cloud_infra_gather_api_data/virtualenv
1. Activate virtual environment

       source cloud_infra_gather_api_data/virtualenv/bin/activate
       # If you get error "virtualenv: command not found", relogin into shell and try again.
1. One can check which virtualenv is in use by:

       echo $VIRTUAL_ENV
       /home/iisti/scripts/cloud_infra_gather_api_data/virtualenv
1. Deactivate (just to know how it's done)

       deactivate

1. Install modules

        # Remember to activate virtualenv before
        pip3 install -r requirements.txt

#### GCP (Google Cloud Providor) instructions
1. Create service account for connecting to GCP API.
    * One can do this also with "Installed Application".
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
    1. Required information from GCP:
       * Service account ID == api_key for Libcloud
       * Project ID, this string can be found from GCP Project Dashboard.
