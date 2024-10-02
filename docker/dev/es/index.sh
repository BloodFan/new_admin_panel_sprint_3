#!/bin/sh

# until curl -sS "elasticsearch:9200/_cat/health?h=status" | grep -q "green\|yellow"; do 
#     sleep 1 
# done

# curl -XPUT http://localhost:9200/table -H 'Content-Type: application/json' -d @/es/movies.json
