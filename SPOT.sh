#!/bin/bash

while getopts "cseib" opt; do
    case $opt in
        c)
            python3.11 -m venv venv
            ;;
        s)
            source venv/bin/activate
            ;;
        e)
            deactivate
            ;;
        i)
            python -m pip install -r requirements.txt
            ;;
        b)
            cd src/lib
            maturin build 
            whl=$(ls target/wheels | grep *.whl)
            python -m pip install $whl
            cd ../../
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            ;;
    esac
done

if [ "$1" == "setup" ]; then
        echo "Setting up virtual environment..." 
        ./SPOT -c
        echo "Starting Virtual Environment..."
        ./SPOT -s
        echo "Installing dependencies..."
        ./SPOT -i
        echo "Building the project..."
        ./SPOT -b
fi