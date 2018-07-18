#!/bin/bash
sudo apt-get update
sudo apt-get install -y python-pip
sudo pip install --upgrade pip
sudo pip install -r farmacia/requirements.txt
