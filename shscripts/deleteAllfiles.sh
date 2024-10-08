#!/bin/bash
echo "Do you really want to delete? Press ENTER to proceed or any other key to cancel."

read -r input
cd ..
if [ -z "$input" ]; then
    find . -type f -name "*.log" -delete
else
    echo "Delete Operation Cancelled."
fi




