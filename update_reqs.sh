#!/bin/bash

if [[ $1 == 'project' ]]
then
    requirements='requirements.txt'
else
    requirements="services/${1}/requirements.txt"
fi

if [[ $2 == 'dry' ]]
then
    command='pur -d -z -r '
else
    command='pur -z -r '
fi

eval $command $requirements

if [[ $? == 10 ]]
then
    exit 0
else
    exit 1
fi
