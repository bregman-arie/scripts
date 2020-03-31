#!/bin/bash

default_json_file="$HOME/os-data-miner/data.json"

# Check for user input
if [ "$#" -lt 1 ]; then
    read -p "The path of the JSON file:[$default_json_file]" json_file
fi

json_file=${json_file:-$default_json_file}

echo "Adjusting data. Please wait..."

# Remove backslashes
sed -i 's/\\//g' $json_file

# Put each json object on its own line
sed -i 's/\"{\"values/\n{\"values/g' $json_file
# sed -i 's/\"\, \[//g' $json_file
sed -i 's/\"]]\, \[//g' $json_file
sed -i 's/}\"\,/}/g' $json_file
sed -i 's/ \[$//g' $json_file

# Remove beginning and end of the file
sed -i '1d' $json_file
sed -i 's/\"\]\]\]$/\n/g' $json_file

# Add index for every json object
sed -i '/values/i { "index" : { "_index" : "usage_patterns"}}' $json_file

# Remove dates
sed -i 's/"20[0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]", //g' $json_file

# Remove empty key:value
sed -i 's/, "": ""//g' $json_file

# Replace True with true
sed -i 's/True/true/g' $json_file

echo "Finished adjusting the data from $json_file"
