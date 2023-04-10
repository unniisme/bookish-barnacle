#!/bin/bash

mkdir -p files
mkdir -p gptHistory

export FLASK_APP="app"
alias test="flask run --host=0.0.0.0 -p 5500 --debug"
alias host="flask run --host=0.0.0.0 -p 5500"