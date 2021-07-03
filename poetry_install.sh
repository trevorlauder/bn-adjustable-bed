#!/bin/bash

(cd src/app-api && poetry update && poetry install)
(cd src/bed-socket && poetry update && poetry install)
(cd src/controller-api && poetry update && poetry install)
