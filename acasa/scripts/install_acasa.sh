#!/bin/bash

# install packages required by acasa
for i in Adafruit-DHT bluepy croniter twython; do
	echo Installing $i...
	pip install $i
done

echo Setting conf file path in util module...
CONF_PATH=$(python -c 'import json; print json.load(open("conf/acasa.conf"))["conf_path"]')
CONF_FILE=$CONF_PATH/acasa.conf
sed -i "s@/opt/acasa/conf/acasa.conf@${CONF_FILE}@g" utility/util.py

ACASA_ROOT=$(python -c 'import json; print json.load(open("../conf/acasa.conf"))["acasa_root"]')
echo Installing acasa into $ACASA_ROOT...
mkdir -p $ACASA_ROOT
cp -r ./* $ACASA_ROOT

echo Cleaning up...
rm -rf ./*

echo Setting the system PYTHONPATH
export PYTHONPATH="${ACASA_ROOT}:${PYTHONPATH}"
echo "export PYTHONPATH=\"${ACASA_ROOT}:${PYTHONPATH}\"" >> ~/.bashrc

echo Starting acasa...
dos2unix $ACASA_ROOT/scripts/scheduler.py
dos2unix $ACASA_ROOT/acasa.sh
chmod +x $ACASA_ROOT/acasa.sh
chmod +x $ACASA_ROOT/scripts/scheduler.py
$ACASA_ROOT/scripts/acasa.sh start

echo Done