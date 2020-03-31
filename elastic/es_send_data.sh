#!/bin/bash

default_json_file="$HOME/os-data-miner/data.json"
default_es_ip="127.0.0.1"

if [ "$#" -lt 1 ]; then
    read -p "The path of the JSON file:[$default_json_file]" json_file
    read -p "The IP address of the elasticsearch instance:[$default_es_ip]" es_ip
fi

json_file=${json_file:-$default_json_file}
es_ip=${es_ip:-$default_es_ip}

curl -H "Content-Type: application/json" -XPOST "$es_ip:9200/usage_patterns/_bulk?pretty&refresh" --data-binary "@$json_file"
