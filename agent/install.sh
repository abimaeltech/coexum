#!/usr/bin/env bash
# Instala dependências em Linux/macOS e configura alias
set -e
sudo apt update && sudo apt install -y python3 python3-pip docker.io git
pip3 install -e .
echo "alias coexum='python3 -m coexum'" >> ~/.bashrc
source ~/.bashrc
