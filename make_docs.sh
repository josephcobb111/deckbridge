#!/bin/bash

cd docs
make clean html latexpdf
cd ../
echo "Execution complete"
