#!/bin/bash

curl -X PUT "http://elasticsearch:9200/movies" -H "Content-Type: application/json" -d @/usr/share/elasticsearch/movies.json