# A live demonstration of NLP Classification with Spacy and FastAI.

## Table of Contents

- [Problem Statement](#problem-statement)
- [Getting Started](#getting-started)
- [Requirements](#requirements)

## Problem Statement

This is a group chat application being rendered with Flask. Real time group messages are enabled with SocketIO, a messaging framework. Messages are tokenized by Spacy for contextual inline formatting. Additionally, FastAI classifiers are used to power emotion and toxicity detection.

## Getting Started

Install [Docker Desktop](https://www.docker.com/products/docker-desktop) and make sure it is running locally.

- From within the current `flaskchat` directory, run `docker-compose up --build` to start application.
- To reset the containers and all data within, run `docker-compose rm` once containers are stopped.
- To enter a running container, run: `docker exec -it <container_name> /bin/bash`.

#### Pre-Commit

Make sure to setup a pre-commit hook in your local repo using the following command: `pre-commit install`

## Requirements

This is intended to run on [Python](https://www.python.org) >= 3.8.2

#### Required Packages

- Flask
- Flask-SocketIO
- eventlet
- numpy
- pandas
- spacy
- fastai
