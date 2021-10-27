#!/bin/bash

rasa visualize -s "./data/my_stories/$1.yml" --out "./data/my_graphs/$1.html"
open "./data/my_graphs/$1.html"
