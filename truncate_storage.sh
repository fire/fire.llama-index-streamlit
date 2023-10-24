#!/bin/bash

# Loop through all json files in the current directory
for file in storage/*.json
do
    # Truncate each file
    echo -n "{}" > $file
done

