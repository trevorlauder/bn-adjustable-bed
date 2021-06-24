#!/bin/bash

conda env update --file conda.yml

bash -l -c "(conda activate bn_adjustable_bed && pip install -r requirements.txt -r services/controller/requirements.txt -r services/bed/requirements.txt -r services/app/requirements.txt)"
