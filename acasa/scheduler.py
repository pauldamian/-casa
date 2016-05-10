'''
Created on 28 mar. 2016

@author: Paul
'''
from datetime import datetime as dt
from datetime import timedelta
import command
from laverdadb import Laverdadb
import sys
import getopt
from resources import USERS
import calendar

db = Laverdadb()

'''
tool de programare a comenzilor
primul ecran: welcome message + selectarea comenzii
2. when? date, time
run once or recurrent?
3. if once: schedule
4. else: how often?

'''
weekdays = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}


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
            if td == 'monthly':
                try:
                    date = date.replace(month=date.month + 1)
                except ValueError:
                    date = date.replace(year=date.year + 1, month=1)
            else:
                date += td
    return dates


def get_valid_input(inp):
    '''
    Checks the custom input for recurrent jobs
    Returns:
        None for * wildcard
        A list of integers, according to the input
    '''
    ints = []
    if inp == '*':
        return None
    else:
        try:
            if '-' in inp:
                s, e = inp.split('-')
                ints = range(s, e)
            elif ',' in inp:
                ints = [int(i) for i in inp.split(',')]
            else:
                ints.append(int(inp))
        except ValueError:
            print "Cannot read input"
        return ints


def main(argv):
    st = None
    user = USERS[0]
    com = ''
    cid = 1
    if len(sys.argv) > 1:
        help_text = '''
USAGE: scheduler.py [options]

if options are not provided, then you will go through a text-based interface
    which allows the scheduling of both one-time and recurrent jobs
else the user can schedule an one-time job directly from the command line
    by providing ALL the following arguments, enclosed in double quotes:
    -c: name of the command (lights, show, cancel) [followed by arguments]
    -t: schedule time in the following format YYYY-MM-DD HH:MM:SS

Example: scheduler.py -c "lights on" -t "2016-05-07 14:43:50"
        '''
        try:
            opts, args = getopt.getopt(argv, "h:c:t:")
        except getopt.GetoptError:
            print help_text
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print help_text
                sys.exit()
            elif opt == '-c':
                com = arg
            elif opt == '-t':
                st = arg
        cid = db.get_static_id()
        res = db.register_command(cid, com, dt.now(), user, schedule=st)
        print res
    else:
        print '''
        Welcome to the Command Scheduler. This tool enables you to schedule jobs,
        either for one-time or recurrent runs.
        Begin by choosing one of the available commands from below:'''
        vc = command.valid_commands
        vc.remove('help')
        print '        ' + str(vc)
        while True:
            com = raw_input('Type the desired command along with its arguments: ')
            if com.split()[0] in vc:
                break
        print '''\n
        Next, set the date and time for the command execution.
        Use the following format: 2000-01-30 21:45:50'''
        while True:
            t = raw_input('Type the desired date: ')
            st = command.valid_date(t)
            if st is not None:
                if st > dt.now():
                    break
        while True:
            once = raw_input('Is this a one-time or a recurrent job? [o/r]: ')
            if once in ['o', 'r']:
                break
        if once == 'o':
            cid = db.get_static_id()
            res = db.register_command(cid, com, dt.now(), user, schedule=str(st))
        else:
            while True:
                ed = raw_input('Please enter the end date: ')
                et = command.valid_date(ed)
                if et is not None:
                    if et > st:
                        break
            while True:
                print '''
        For the recurrence part, you can use keywords as:
        every [minute/hour/day/<weekday_name>/week/month]
        or use the following format with integers:
        [year] [month] [day] [weekday] [hour] [minute] [second]
        you can use the * wildcard for all values and specify ranges using -
        Example: to run a command every Sunday at noon:
        every Sunday (after setting the start time to 12:00:00)
        * * * 7 12 0 0
                '''
                recurrence = []
                rec = raw_input('Set recurrence: ').lower()
                if rec.split()[0] == 'every':
                    cate = rec.split()[1]
                    if cate == 'minute':
                        recurrence.append(timedelta(minutes=1))
                    elif cate == 'hour':
                        recurrence.append(timedelta(hours=1))
                    elif cate == 'day':
                        recurrence.append(timedelta(days=1))
                    elif cate[:3].capitalize() in weekdays.keys():
                        dd = (weekdays[cate[:3].capitalize()] - st.isoweekday()) % 7
                        st = st.replace(day=st.day + dd)
                        recurrence.append(timedelta(days=7))
                    elif cate == 'week':
                        recurrence.append(timedelta(days=7))
                    elif cate == 'month':
                        recurrence.append('monthly')
                    dl = generate_dates(st, et, recurrence)
                    for d in dl:
                        cid = db.get_static_id()
                        res = db.register_command(cid, com, dt.now(), user, schedule=str(d))
                        print res
                else:
                    try:
                        y, mo, d, w, h, mi, s = rec.split()
                        ly = get_valid_input(y)
                        if ly is not None:
                            if len(ly) == 1:
                                st = st.replace(year=ly[0])
                        else:
                            ly = range(st.year, et.year + 1)
                        lmo = get_valid_input(mo)
                        if lmo is not None:
                            if len(lmo) == 1:
                                st = st.replace(month=lmo[0])
                        else:
                            lmo = range(st.month, et.month + 1)
                        ld = get_valid_input(d)
                        if ld is not None:
                            if len(ld) == 1:
                                st = st.replace(day=ld[0])
                        else:
                            ld = range(st.year, et.year + 1)
                        lw = get_valid_input(w)
                        if lw is None:
                            lw = range(1, 8)
                        lh = get_valid_input(h)
                        if lh is not None:
                            if len(lh) == 1:
                                st = st.replace(hour=lh[0])
                        else:
                            if st.date() != et.date():
                                lh = range(0, 24)
                            else:
                                lh = range(st.hour, et.hour + 1)
                        ly = get_valid_input(y)
                        if ly is not None:
                            if len(ly) == 1:
                                st = st.replace(year=ly[0])
                        else:
                            ly = range(st.year, et.year + 1)
                        ly = get_valid_input(y)
                        if ly is not None:
                            if len(ly) == 1:
                                st = st.replace(year=ly[0])
                        else:
                            ly = range(st.year, et.year + 1)
                    except ValueError as ve:
                        print ve.message

                break
                    
if __name__ == "__main__":
    main(sys.argv[1:])
