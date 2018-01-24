#!/bin/bash

usage() {
	echo "Usage: $0 {start|stop|restart|status} [component]" >&2 
	echo "	component in [executor, reader, communicator]" >&2
}

if [ -z "${1}" ]; then
	usage
	exit 1
fi

log_dir="/var/log/acasa/"

if [[ ! -d "${log_dir}" ]]; then
	echo "Creating log directory"
	mkdir ${log_dir}
fi

PROG="acasa"
if [[ ${2} ]]; then
    if [[ ${2} == "communicator" || ${2} == "executor" || ${2} == "reader" ]]; then
    	PROG=$2;
    	PIDFILE=${log_dir}${PROG}.pid;
    else
	echo "Invalid component name"
	usage
	exit 1
    fi
fi

start_component() {
	echo "Starting ${1} (PID written to ${log_dir}${1}.pid)."
  	python -m lib.${1} & echo $! > "${log_dir}${1}.pid"
}

start_watchdog() {
	echo "Starting watchdog process. (PID written to ${log_dir}watchdog.pid)."
	./watchdog & echo $! > "${log_dir}watchdog.pid"
}

start() {
  if [ ${PROG} == "acasa" ]; then
	start_component executor;
	start_component communicator;
	start_component reader;
	start_watchdog;
  else
	start_component ${PROG};
  fi
}

status_component() {
  PID=$(cat "${log_dir}${1}.pid");
  if [[ -z "${PID}" ]]; then
    echo "${1} is not running (missing PID)."
  elif [[ -e /proc/${PID}/exe ]]; then 
    echo "${1} is running (PID: ${PID})."
  else
    echo "${1} is not running (tested PID: ${PID})."
  fi
}

status() {
  if [ ${PROG} == "acasa" ]; then
    status_component executor
    status_component reader
    status_component communicator
  else
    status_component ${PROG}
  fi
}

stop_component() {
  PID=$(cat "${log_dir}${1}.pid");
  PIDFILE=${log_dir}$1.pid
  if [[ -z "${PIDFILE}" ]]; then
    echo "${1} is not running (missing PID)."
  elif [[ -e /proc/${PID}/exe ]]; then 
    echo "Stopping ${1}"
    kill ${PID} &
    > ${PIDFILE}
    echo "${1} stopped"
  else
    echo "${1} is not running (tested PID: ${PID})."
  fi

}

stop() {

  if [ ${PROG} == "acasa" ]; then
  	stop_component watchdog;
	stop_component communicator;
	stop_component reader;
	stop_component executor;
  else
	stop_component ${PROG}
  fi
}


case "$1" in
  start)
        $1;
        ;;
  restart)
        stop; sleep 1; start;
        ;;
  stop)
        stop ${PROG};
        ;;
  status)
        status ${PROG};
        ;;
  *)
        usage;
        exit 4
        ;;
esac

exit 0
