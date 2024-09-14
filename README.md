# LineToXml

## How to setup
Setup a python virtual environment and install requirements

    python3 -m venv venv

    . ./venv/bin/activate

    python3 -m pip install -r requirements.txt

## Run test cases
    python3 -m pytest

## Check code style
    python3 -m flake8

## Run the converter
The converter can be run from the command line

    python3 main.py example/input.txt [output_file.xml]
