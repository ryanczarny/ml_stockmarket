#!/bin/bash

for ((n=0;n<5000000000;n++))
do
 python3 page_scrape.py
 sleep 300s
done