# gist.github.com/rodw/3345668
#!/bin/bash

usage() {
	echo "Usage: $0 {start|stop|restart|status} [component]" >&2 
	echo "	component in [executor, reader, twitter]" >&2
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
    if [[ ${2} == "twitter" || ${2} == "executor" || ${2} == "reader" ]]; then
    	PROG=$2;
    	PIDFILE=${log_dir}${PROG}.pid;
	echo $PIDFILE
    else
	echo "Invalid component name"
	usage
	exit 1
    fi
fi

star() {
	echo "Starting ${1} (PID written to ${log_dir}${1}.pid)."
  	python -c "import ${1}; ${1}.run()" & echo $! > "${log_dir}${1}.pid"
}
start() {
  if [ ${PROG} == "acasa" ]; then
	star executor;
	star twitter;
	star reader;
  else
	star ${PROG};
  fi
}

status() {
  PID=$(cat "${log_dir}${1}.pid");
  if [[ -z "${PID}" ]]; then
    echo "${1} is not running (missing PID)."
  elif [[ -e /proc/${PID}/exe ]]; then 
    echo "${1} is running (PID: ${PID})."
  else
    echo "${1} is not running (tested PID: ${PID})."
  fi
}

stat() {
  if [ ${PROG} == "acasa" ]; then
    status executor
    status reader
    status twitter
  else
    status ${PROG}
  fi
}

stop() {
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

stp() {

  if [ ${PROG} == "acasa" ]; then
	stop twitter;
	stop reader;
	stop executor;
  else
	stop ${PROG}
  fi
}


case "$1" in
  start)
        $1;
        ;;
  restart)
        stp; sleep 1; start;
        ;;
  stop)
        stp ${PROG};
        ;;
  status)
        stat ${PROG};
        ;;
  *)
        usage;
        exit 4
        ;;
esac

exit 0
