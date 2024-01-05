#! /usr/bin/bash
# Copyright (C) 2024-present by Rohith-Sreedharan@Springreen, < https://github.com/sprin-g-reen >.
#
# This file is part of < https://github.com/rohith-sreedharan/Charu-DR-Model > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/rohith-sreedharan/Charu-DR-Model >
#
# All rights reserved.

echo -e "\e[1mChecking for requirement updates...\e[0m"
pip install -r requirements.txt --upgrade > /dev/null 2>&1

if [ -f "runtime.txt" ]; then
    python_version=$(cat runtime.txt)
    echo -e "\e[1mChecking Python version...\e[0m"
    if [ "$python_version" != "$(python --version 2>&1 | awk '{print $2}')" ]; then
        echo -e "\e[1mUpdating Python version to $python_version...\e[0m"
        pyenv install $python_version > /dev/null 2>&1
        pyenv global $python_version > /dev/null 2>&1
        echo -e "\e[1mPython version updated successfully!\e[0m"
    else
        echo -e "\e[1mPython version is up to date.\e[0m"
    fi
else
    echo -e "\e[1mNo runtime file found. contact admin, Skipping Python version check.\e[0m"
fi

echo -e "\e[1;32mProject Intilized successfully!\e[0m"


echo -e "\e[1mStarting app.py...\e[0m"
python3 app.py
