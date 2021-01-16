<!-- cSpell:ignore mkdbuttons, nsdname, ostc -->
<!-- cSpell:words Elspeth, vnet, nics, mkdir,  -->
<!-- cSpell:enableCompoundWords -->

# Additional notes for setting up a server on Ubuntu 18.04 LTS

Refer to Chapter 9 of _Test-Driven Development with Python_

Anthony Montague _16 January 2021_

## Installing Python 3.8

Ubuntu 18.04 comes with Python 3.6 installed, but defaults to Python 2.
The default Ubuntu repositories do have Python 3.8, but only 3.8.0 so will
will continue to use the 'deadsnakes' repository

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.8 python3.8-venv

# update-alternatives: --install needs <link> <name> <path> <priority>
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 100
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 200

# Check for 3.8.7 or higher
python --version
```
