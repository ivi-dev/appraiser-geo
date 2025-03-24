#!/bin/bash

# ==========================================================
# PREPARE THE APP'S DEV CONTAINER'S ENVIRONMENT POST CREATE
# ==========================================================


# 1. Install the declared dependencies
pip install -r requirements.txt

# 2. Update the package manager's lists
sudo apt update

# 3. Install dos2unix (line-endings converter)
sudo apt install -y dos2unix

# 4. Convert the line-endings of all .sh scripts 
# in ./scripts to Unix ones
dos2unix ./scripts/*.sh -v

# 5. Make every .sh script in ./scripts executable
# by its author an group
sudo chmod ug+x ./scripts/*.sh
