#!/bin/bash

echo "Uninstalling pr0t3ct \n"

echo "Do you really want to uninstall pr0t3ct ? (y/n)"
read option

if [option == 'y']
then
	rm -rf dep
	rm -rf Output
	rm pr0t3ct.py
else
	echo "Aborted"
	