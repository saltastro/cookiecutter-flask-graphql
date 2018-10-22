#!/usr/bin/env bash

if [[ "{{ cookiecutter.open_source_license }}" = "Not open source" ]]
then
    rm LICENSE
fi

if [[ "{{ cookiecutter.install_requirements }}" = "yes" ]]
then
    echo "Creating a virtual environment"
    python3 -m venv venv
    source venv/bin/activate
    if [[ $? != 0 ]]
    then
        exit 1
    fi
    pip install -r requirements-to-freeze.txt
    pip freeze > requirements.txt

    echo
    echo "A virtual environment venv with the required packages has been created in the project's root folder."
fi

echo
echo "Please see the README on"
echo
echo "https://github.com/saltastro/cookiecutter-flask-graphql"
echo
echo "for details on how to get started."
echo
echo "TL;DR"
echo
echo "cd {{ cookiecutter.project_slug }}"
{% if cookiecutter.install_requirements == "yes" %}
echo "source venv/bin/activate"
{% else %}
echo "python3 -m venv venv"
echo "source venv/bin/activate"
echo "pip install -r requirements-dev.txt"
echo "pip freeze > requirements.txt"
{% endif %}
echo "make help"
echo "# set environment variables before executing the next command"
echo "make start"

