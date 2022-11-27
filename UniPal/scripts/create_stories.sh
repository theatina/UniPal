#!/bin/bash

# rasa visualize -s "./data/my_stories/$1.yml" --out "./data/my_graphs/$1.html"
# open "./data/my_graphs/$1.html"

# Set-Location "C:/Users/Theatina/Documents/Gdrive_ctkyl/Studies/Di_Master/Di_NLP/Courses/3rd_Semester/M913_Διαλογικά_Συστήματα_και_Φωνητικοί_Βοηθοί/Project/Rasa_Data"

if [ $# -ne 0 ]; then
    if [[ $1 = "UniPal" || $1 = "SocioPal" ]]; then
        domain=$1
        echo "graph path: ../hw1/my_graphs/$domain.html"
        rasa visualize -s "../hw1/my_stories/$domain.yml" --out "../hw1/my_graphs/$domain.html"
        open '../hw1/my_graphs/$domain.html'
    elif [ $1 -eq "test" ]; then
        echo "graph path: ../hw1/my_graphs/test_stories.html"
        rasa visualize -s "./tests/test_stories.yml" --out "../hw1/my_graphs/test_stories.html"
          
    else
        echo ERROR: Unknown Dialogue System was given as argument! $'\n\n'Available Dialogue Systems: $'\n'1. UniPal$'\n'2. SocioPal
    fi

else
    echo $'\n' ERROR: No arguments were given ! $'\n'
fi


echo " "
