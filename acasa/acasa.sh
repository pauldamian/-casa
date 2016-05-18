# gist.github.com/rodw/3345668
#!/bin/bash

usage() {
	echo "Usage: 'basename $0' {start|stop|restart|status} [component]" >&2 
	echo "	component in [executor, reader, twitter]" >&2
}

if [ -z "${1}" ]; then
	usage
	exit 1
fi

PIDFILE_E="executor.pid"
PIDFILE_R="reader.pid"
PIDFILE_T="twitter.pid"
PROG="acasa"

if [[ ${2} ]]; then
  # if [[ "${2}" == "executor"]]; then
    PROG=$2;
  #fi
fi

# Get the PID from PIDFILE if we don't have one yet.
if [[ -z "${PID_S}" && -e ${PIDFILE_S} ]]; then
  PID_S=$(cat ${PIDFILE_S});
fi

if [[ -z "${PID_T}" && -e ${PIDFILE_T} ]]; then
  PID_T=$(cat ${PIDFILE_T});
fi

if [[ -z "${PID_E}" && -e ${PIDFILE_E} ]]; then
  PID_E=$(cat ${PIDFILE_E});
fi


start_e() {
  echo "Starting executor (PID written to $PIDFILE_E)."
  python -c "import executor; executor.run()" & echo $! > ${PIDFILE_E}
}

start_r() {
  echo "Starting reader (PID written to $PIDFILE_R)."
  python -c "import reader; reader.run()" & echo $! > ${PIDFILE_R}
}
start_t() {
  echo "Starting twitter (PID written to $PIDFILE_T)."
  python -c "import twitter; twitter.run()" & echo $! > ${PIDFILE_T}
}
start() {
  if [ ${PROG} == "executor" ]; then
	start_e
  elif [  ${PROG} == "reader" ]; then
	start_r
  elif [ ${PROG} == "twitter" ]; then
    start_t
  elif [ ${PROG} == "acasa" ]; then
	start_t;
	start_r;
	start_e;
  else
	echo "${2} is not a valid component"
  fi
}

status() {
  if [[ -z "${PID}" ]]; then
    echo "${PROG} is not running (missing PID)."
  elif [[ -e /proc/${PID}/exe ]]; then 
    echo "${PROG} is running (PID: ${PID})."
  else
    echo "${PROGSHORT} is not running (tested PID: ${PID})."
  fi
}

stop_e() {
  if [[ -z "${PID_E}" ]]; then
    echo "executor is not running (missing PID)."
  elif [[ -e /proc/${PID_E}/exe ]]; then 
    kill $1 ${PID_E}
  else
    echo "executor is not running (tested PID: ${PID_E})."
  fi
}

stop_t() {
  if [[ -z "${PID_T}" ]]; then
    echo "twitter is not running (missing PID)."
  elif [[ -e /proc/${PID_T}/exe ]]; then 
    kill $1 ${PID_T}
  else
    echo "twitter is not running (tested PID: ${PID})."
  fi
}

stop_r() {
  if [[ -z "${PID_R}" ]]; then
    echo "reader is not running (missing PID)."
  elif [[ -e /proc/${PID}/exe ]]; then 
    kill $1 ${PID}
  else
    echo "reader is not running (tested PID: ${PID})."
  fi
}

stop() {
  if [[ -z "${PID_E}" ]]; then
    echo "${PROGSHORT} is not running (missing PID)."
  elif [[ -e /proc/${PID_E}/exe ]]; then 
    kill $1 ${PID_E}
  else
    echo "Process is not running (tested PID: ${PID})."
  fi
}

case "$1" in
  start)
        start;
        ;;
  restart)
        stop; sleep 1; start;
        ;;
  stop)
        stop;
        ;;
  force-stop)
        stop -9
        ;;
  force-restart)
        stop -9; sleep 1; start;
        ;;
  status)
        status;
        ;;
  *)
        usage;
        exit 4
        ;;
esac

exit 0
