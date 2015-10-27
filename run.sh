#!/bin/bash
filename=$1
allfiles=""
python_file_path="/home/aadarsh-ubuntu/Desktop/Summer Projs/CMDUtility/drive.py"
if [ -z "$filename" ]; then
	echo "filename is empty"
else
	for var in "$@"
	do
		allfiles="$allfiles $var"
	done
	#Call python program to upload files
	#python /home/aadarsh-ubuntu/Desktop/Summer' 'Projs/CMDUtility/drive.py$allfiles
	python "$python_file_path"$allfiles
fi
