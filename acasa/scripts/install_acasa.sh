#!/bin/bash
echo Stopping acasa...
acasa stop || echo acasa already stopped

DEFAULT_CONF_FILE="/etc/acasa/acasa.conf"
# Moving up a level
cd ..

if [[ ${1} == "upgrade" ]]; then
	CONF_FILE=$DEFAULT_CONF_FILE
else
	mv $DEFAULT_CONF_FILE $DEFAULT_CONF_FILE.back
	CONF_PATH=$(python -c 'import json; print json.load(open("conf/acasa.conf"))["conf_path"]')
	CONF_FILE=$CONF_PATH/acasa.conf
	# install packages required by acasa
	for i in Adafruit-DHT bluepy croniter twython; do
		echo Installing $i...
		pip install $i
	done
fi

echo Setting conf file path in util module...
sed -i "s@/etc/acasa/acasa.conf@${CONF_FILE}@g" utility/util.py

ACASA_ROOT=$(python -c "import json; print json.load(open('"${CONF_FILE//\'/\\\'}"'))['acasa_root']")
echo Removing old modules...
rm -rf $ACASA_ROOT

echo Installing acasa into $ACASA_ROOT...
mkdir -p $ACASA_ROOT
if [[ ${1} == "upgrade" ]]; then
	rm -rf conf
else
	mkdir -p $CONF_PATH; mv conf $CONF_PATH
fi

cp -r ./* $ACASA_ROOT

echo Cleaning up...

rm -rf ./*

echo Setting the system PYTHONPATH
export PYTHONPATH="${ACASA_ROOT}:${PYTHONPATH}"
echo "export PYTHONPATH=\"${ACASA_ROOT}:${PYTHONPATH}\"" >> ~/.bashrc

dos2unix $ACASA_ROOT/scripts/scheduler.py
dos2unix $ACASA_ROOT/acasa.sh
chmod +x $ACASA_ROOT/acasa.sh
chmod +x $ACASA_ROOT/scripts/scheduler.py

echo Making acasa available to all users
ln -s $ACASA_ROOT/acasa.sh /usr/local/bin/acasa || echo acasa is available to all users

echo Starting acasa...
acasa start

echo Done