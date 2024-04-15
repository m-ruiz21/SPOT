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
            ls
            ;;
        b)
            cd src/lib
            #maturin develop --release 
            maturin build
            python -m pip install target/wheels/$(ls target/wheels | grep .whl$)
            cd ../../
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            ;;
    esac
done

if [ "$1" == "setup" ]; then
        echo "Installing Rust..."
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
        echo "Installing Python3.11 Using Brew"
        brew install python@3.11
        echo "Setting up virtual environment..." 
        ./SPOT -c
        echo "Starting Virtual Environment..."
        ./SPOT -s
        echo "Installing dependencies..."
        ./SPOT -i
        echo "Building the project..."
        ./SPOT -b
fi