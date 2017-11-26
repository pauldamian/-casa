#!/usr/bin/python
import sys
import getopt
from datetime import datetime as dt
from datetime import timedelta
from croniter import croniter

from lib import util
from lib import command
from lib.todo import Todo
from lib import constants
from __builtin__ import str

USERS = util.get_conf_value(constants.KEY_USERS)
WEEKDAYS = {"Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6, "Sun": 7}

db = Todo()


def generate_dates(start_date, end_date, recurrence):
    """
    This function is used to generate the list of schedule times
    for the recurring commands.
    Arguments:
        start_date - datetime object denoting the first occurrence of the command
        stop_date - datetime object denoting the last time the command can be executed
        recurrence - a list of timedelta objects which specify the interval at which jobs take place
    Returns a list of datetime objects
    """
    dates = []
    date = start_date
    for td in recurrence:
        while date <= end_date:
            dates.append(date)
            if td == "monthly":
                try:
                    date = date.replace(month=date.month + 1)
                except ValueError:
                    date = date.replace(year=date.year + 1, month=1)
            else:
                date += td
    return dates


def get_valid_input(inp):
    """
    Checks the custom input for recurrent jobs
    Returns:
        None for * wildcard
        A list of integers, according to the input
    """
    ints = []
    if inp == "*":
        return None
    else:
        try:
            if "-" in inp:
                s, e = inp.split("-")
                ints = range(s, e)
            elif "," in inp:
                ints = [int(i) for i in inp.split(",")]
            else:
                ints.append(int(inp))
        except ValueError:
            print "Cannot read input"
        return ints


def main(argv):
    st = None
    user = USERS[0]
    com = ""
    if len(sys.argv) > 1:
        help_text = """
USAGE: scheduler.py [options]

if options are not provided, then you will go through a text-based interface
    which allows the scheduling of both one-time and recurrent jobs
else the user can schedule an one-time job directly from the command line
    by providing ALL the following arguments, enclosed in double quotes:
    -c: name of the command (lights, show, cancel) [followed by arguments]
    -t: schedule time in the following format YYYY-MM-DD HH:MM:SS

Example: scheduler.py -c "lights on" -t "2016-05-07 14:43:50"
        """
        try:
            opts, _ = getopt.getopt(argv, "h:c:t:")
        except getopt.GetoptError:
            print help_text
            sys.exit(2)
        for opt, arg in opts:
            if opt == "-h":
                print help_text
                sys.exit()
            elif opt == "-c":
                com = arg
            elif opt == "-t":
                st = arg
        if st == "now" or st is None:
            st = str(dt.now()).split(".")[0]

        cmd = command.Command(com, user, schedule=st)
        db.insert_command(cmd)

    else:
        print """
    Welcome to the Command Scheduler. This tool enables you to schedule jobs,
    either for one-time or recurrent runs.
    Begin by choosing one of the available commands from below:"""
        vc = command.valid_commands
        print "        " + str(vc)
        while True:
            com = raw_input("Type the desired command along with its arguments: ")
            if com.split()[0] in vc:
                break
        print """
    Next, set the date and time for the command execution.
    Use the following format: 2000-01-30 21:45:50"""
        while True:
            t = raw_input("Type the desired date: ")
            st = command.valid_date(t)
            if st is not False:
                if st > dt.now():
                    break
        while True:
            once = raw_input("Is this a one-time or a recurrent job? [o/r]: ")
            if once in ["o", "r"]:
                break
        if once == "o":
            cmd = command.Command(com, user, schedule=st)
            db.insert_command(cmd)
        else:
            while True:
                ed = raw_input("Please enter the end date: ")
                try:
                    et = command.valid_date(ed)
                    if et > st:
                        break
                    else:
                        print "End date is smaller than start date!"
                except ValueError, ve:
                    print ve
            print """
        For the recurrence part, you can use keywords as:
        every [minute/hour/day/<weekday_name>/week/month]
        or use the following cron format:
        [minute] [hour] [day] [month] [day_of_week] [seconds]
        you can use the * wildcard for all values and specify ranges using -
        Example: to run a command every Sunday at noon:
        every Sunday (after setting the start time to 12:00:00)
        0 12 * * 7 0
                """
            while True:
                recurrence = []
                rec = raw_input("Set recurrence: ").lower()
                if rec.split()[0] == "every":
                    cate = rec.split()[1]
                    try:
                        increment = int(cate)
                        cate = rec.split()[2][:-1]
                    except ValueError:
                        increment = 1
                    except IndexError:
                        print "You need to provide more arguments (the unit of time, most likely)"

                    if cate == "minute":
                        recurrence.append(timedelta(minutes=increment))
                    elif cate == "hour":
                        recurrence.append(timedelta(hours=increment))
                    elif cate == "day":
                        recurrence.append(timedelta(days=increment))
                    elif cate == "month":   # months keyword not supported yet
                        recurrence.append("monthly")
                    elif cate[:3].capitalize() in WEEKDAYS.keys():
                        dd = (WEEKDAYS[cate[:3].capitalize()] - st.isoweekday()) % 7
                        st = st.replace(day=st.day + dd)
                        recurrence.append(timedelta(days=7 * increment))
                    elif cate == "week":
                        recurrence.append(timedelta(days=7 * increment))
                    else:
                        print "Unsupported unit of time"
                    if len(recurrence) > 0:
                        dl = generate_dates(st, et, recurrence)
                        for d in dl:
                            try:
                                cmd = command.Command(com, user, schedule=str(d))
                                db.insert_command(cmd)
                            except ValueError, ve:
                                print ve
                            print ".",
                        break
                else:
                    try:
                        itr = croniter(rec, st)
                        nt = itr.get_next(dt)
                        while nt <= et:
                            try:
                                cmd = command.Command(com, user, schedule=str(nt))
                                db.insert_command(cmd)
                            except ValueError, ve:
                                print ve
                            nt = itr.get_next(dt)
                            print ".",
                        break
                    except ValueError as ve:
                        print ve.message
    print "Done"


if __name__ == "__main__":
    main(sys.argv[1:])
