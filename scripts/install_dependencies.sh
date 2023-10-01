#!/bin/bash

set -eux

function setup {
    apt update
    apt install software-properties-common aria2 screen -y
    dpkg --add-architecture i386
    mkdir -p ~/.steam/sdk64
}

function install_steamcmd {
    apt install lib32gcc-s1 steamcmd -y
}

echo "This script is meant to be run as root."
setup
install_steamcmd