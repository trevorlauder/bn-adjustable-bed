#!/bin/bash

(cd src/app-api && rm -rf .venv && poetry update && poetry install)
(cd src/bed-socket && rm -rf .venv && poetry update && poetry install)
(cd src/controller-api && rm -rf .venv && poetry update && poetry install)
