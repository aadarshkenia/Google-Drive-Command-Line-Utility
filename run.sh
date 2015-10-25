#!/bin/bash
filename=$1
allfiles=""
if [ -z "$filename" ]; then
	echo "filename is empty"
else
	for var in "$@"
	do
		allfiles="$allfiles $var"
	done
	#Call python program to upload files
	python drive.py"$allfiles"
fi
