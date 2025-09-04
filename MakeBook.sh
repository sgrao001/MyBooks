#!/bin/bash

# Simple script to run specified OOT version
VERSION="$1"  # Get first argument (e.g., ootpv1)

# Run the Python script with the JSON config
echo "  "

python3 "${VERSION}.py" "oot/oot.json" | tee log.out
# Check if Python script succeeded
if [ $? -eq 0 ]; then
    echo "OOT----PASS----" | tee -a log.out
else
    echo "OOT----FAIL----" | tee -a log.out
    exit 1
fi
echo "  "


python3 "${VERSION}.py" "akka/akka.json" | tee -a log.out
# Check if Python script succeeded
if [ $? -eq 0 ]; then
    echo "AKKA----PASS----" | tee -a log.out
else
    echo "AKKA----FAIL----" | tee -a log.out
    exit 1
fi
echo "  "

python3 "${VERSION}.py" "tom/tom.json" | tee -a log.out
# Check if Python script succeeded
if [ $? -eq 0 ]; then
    echo "TOM----PASS----" | tee -a log.out
else
    echo "TOM----FAIL----" | tee -a log.out
    exit 1
fi
echo "  "


python3 "${VERSION}.py" "booklist/booklist.json" | tee -a log.out
# Check if Python script succeeded
if [ $? -eq 0 ]; then
    echo "BOOKLIST----PASS----" | tee -a log.out
else
    echo "BOOKLIST----FAIL----" | tee -a log.out
    exit 1
fi
echo "  "

python3 "${VERSION}.py" "test/test.json" | tee -a log.out
# Check if Python script succeeded
if [ $? -eq 0 ]; then
    echo "TEST----PASS----" | tee -a log.out
else
    echo "TEST----FAIL----" | tee -a log.out
    exit 1
fi
echo "  "

#for file in *.jpg; do
#    mv "$file" "${file%.jpg}.jpeg"
#done

sudo rm /Library/WebServer/Documents/*.html /Library/WebServer/Documents/*.jpg /Library/WebServer/Documents/*.jpeg
sudo cp oot/*.html oot/*.jpeg /Library/WebServer/Documents/.
sudo cp tom/*.html tom/*.jpeg /Library/WebServer/Documents/.
sudo cp akka/*.html akka/*.jpeg /Library/WebServer/Documents/.
sudo cp booklist/*.html booklist/*.jpeg /Library/WebServer/Documents/.
sudo cp test/*.html test/*.jpeg /Library/WebServer/Documents/.
sudo chmod 777 /Library/Webserver/Documents/*

