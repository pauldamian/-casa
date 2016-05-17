# gist.github.com/rodw/3345668

usage() {
	echo "Usage: 'basename $0' {start|stop|restart|status} [component]" >&2 
	echo "	component in [executor, reader, twitter]" >&2
}

if [[ -z "${1}"]]; then
	usage
	exit 1
fi



python -c "import executor; executor.run()" &
python -c "import twitter; twitter.run()" &
python -c "import reader; reader.run()" &