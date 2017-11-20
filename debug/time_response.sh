#!/bin/bash

# Define output format
cat << EOT > curl-output-format.txt

    time_namelookup:  %{time_namelookup}\n
       time_connect:  %{time_connect}\n
    time_appconnect:  %{time_appconnect}\n
   time_pretransfer:  %{time_pretransfer}\n
      time_redirect:  %{time_redirect}\n
 time_starttransfer:  %{time_starttransfer}\n
                    ----------\n
         time_total:  %{time_total}\n
EOT

# Check time response to given server
curl -w "@curl-output-format.txt" -o /dev/null -s $1

# Remove output format file
rm curl-output-format.txt
